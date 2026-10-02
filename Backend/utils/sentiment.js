const https = require("https");

const GEMINI_API_KEY = process.env.GEMINI_API_KEY;
const GEMINI_API_URL = `https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key=${GEMINI_API_KEY}`;



function postJson(url, options) {
    return new Promise((resolve, reject) => {
        const req = https.request(url, options, (res) => {
            let data = "";
            res.on("data", (chunk) => { data += chunk; });
            res.on("end", () => {
                resolve({
                    ok: res.statusCode >= 200 && res.statusCode < 300,
                    status: res.statusCode,
                    body: data
                });
            });
        });
        req.on("error", reject);
        req.write(options.body);
        req.end();
    });
}

/**
 * Uses Gemini AI to analyze a post for urgency, toxicity, and field categorization
 * based on the zero-shot multimodal grievance classification framework.
 */
exports.analyzePostWithAI = async (content) => {
    try {
        const prompt = `Analyze the following user post from a women safety and support community app. 
Evaluate it based on the following criteria:
1. Urgency: How urgent is this post? 
   - green: Normal, sharing a story, general question, no immediate danger.
   - yellow: Concerning, seeking immediate advice, distress, emotional pain.
   - red: Extremely urgent, ONLY use this for active suicidal ideation, active severe physical abuse, or immediate life-threatening situations. DO NOT use red for general complaints or past trauma.
2. Toxicity: Is this post highly toxic or abusive towards others, or does it promote unethical content (e.g. killing someone, intense self-harm, hate speech)?
   - low: Normal, supportive.
   - medium: Some swearing or heated emotion.
   - high: Extremely unethical, violent threats, promoting harm. ONLY use high if the post must be deleted to protect users.
3. Field: What is the main topic/field of this post? Use a concise term like: "Harassment", "Domestic Violence", "Stalking", "Mental Health", "Cyberbullying", "General Safety", etc.

Respond ONLY with a valid JSON object matching this structure:
{
  "urgencyColor": "green" | "yellow" | "red",
  "toxicityLevel": "low" | "medium" | "high",
  "field": "Category String"
}

Post Content: "${content.replace(/"/g, '\\"')}"`;

        const requestBody = JSON.stringify({
            contents: [{ parts: [{ text: prompt }] }],
            generationConfig: {
                temperature: 0.2,
            }
        });

        const options = {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Content-Length": Buffer.byteLength(requestBody)
            },
            body: requestBody
        };

        const response = await postJson(GEMINI_API_URL, options);
        if (!response.ok) {
            console.error("Gemini AI Sentiment Error:", response.body);
            throw new Error("API failed");
        }

        const data = JSON.parse(response.body);
        const textResponse = data.candidates[0].content.parts[0].text;
        
        let jsonStr = textResponse.trim();
        if (jsonStr.startsWith("```json")) {
            jsonStr = jsonStr.substring(7, jsonStr.length - 3);
        } else if (jsonStr.startsWith("```")) {
            jsonStr = jsonStr.substring(3, jsonStr.length - 3);
        }

        const result = JSON.parse(jsonStr);

        // Map toxicity to deletion logic
        const isDeleted = result.toxicityLevel === "high";
        const deletedReason = isDeleted ? "Deleted due to unethical content" : "";
        const suggestSOS = result.urgencyColor === "red";

        return {
            urgencyColor: result.urgencyColor || "green",
            toxicityLevel: result.toxicityLevel || "low",
            field: result.field || "General Safety",
            isDeleted,
            deletedReason,
            suggestSOS
        };
    } catch (err) {
        console.error("Failed to analyze sentiment with AI, falling back to defaults", err);
        // Fallback logic
        return {
            urgencyColor: "green",
            toxicityLevel: "low",
            field: "General Safety",
            isDeleted: false,
            deletedReason: "",
            suggestSOS: false
        };
    }
};
/**
 * Synchronous keyword-based analysis for quick chatbot responses
 */
exports.analyze = (message) => {
    const msg = message.toLowerCase();
    
    // High urgency keywords
    const highUrgency = ["kill", "die", "suicide", "murder", "rape", "weapon", "gun", "knife", "attacked", "bleeding"];
    if (highUrgency.some(word => msg.includes(word))) {
        return "high";
    }

    // Medium urgency keywords
    const mediumUrgency = ["scared", "unsafe", "follow", "harass", "stalk", "help", "danger", "threat", "abuse"];
    if (mediumUrgency.some(word => msg.includes(word))) {
        return "medium";
    }

    return "normal";
};

/**
 * Suggests actions based on the detected urgency level
 */
exports.suggestActions = (level) => {
    switch (level) {
        case "high":
            return [
                "Call 112 immediately",
                "Use the SOS button in the app",
                "Women Helpline: 1091",
                "Find a safe, public place"
            ];
        case "medium":
            return [
                "Move to a crowded area",
                "Share live location with a trusted contact",
                "Call a friend or family member",
                "Talk to our volunteers in the Feed section"
            ];
        default:
            return [
                "Browse safety tips in the app",
                "Check out community stories",
                "Learn about your legal rights",
                "Stay connected with local volunteers"
            ];
    }
};
