const https = require("https");
const Story = require("../models/Story");

const GEMINI_API_KEY = process.env.GEMINI_API_KEY || "AIzaSyD5QwUhjz_b1Wm65O9qPDdU-vYuCW0lS-4";
const GEMINI_API_URL = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${GEMINI_API_KEY}`;

function postJson(url, options) {
    return new Promise((resolve, reject) => {
        const { headers, body } = options;
        const request = https.request(
            url,
            {
                method: "POST",
                headers: {
                    ...headers,
                    "Content-Length": Buffer.byteLength(body)
                }
            },
            (response) => {
                let rawBody = "";
                response.setEncoding("utf8");
                response.on("data", (chunk) => {
                    rawBody += chunk;
                });
                response.on("end", () => {
                    let parsed = null;
                    try {
                        parsed = rawBody ? JSON.parse(rawBody) : null;
                    } catch (error) {
                        parsed = null;
                    }
                    resolve({
                        ok: response.statusCode >= 200 && response.statusCode < 300,
                        status: response.statusCode || 500,
                        rawBody,
                        json: parsed
                    });
                });
            }
        );

        request.on("error", reject);
        request.write(body);
        request.end();
    });
}

exports.getBlogs = async (req, res) => {
    try {
        const query = req.query.query || "women safety and community support";
        
        const prompt = `Use Google Search to find exactly 3 real, up-to-date blog articles or news reports related to "${query}" that are helpful for a women's safety app.
Return ONLY a valid JSON array. Each object in the array must have these exact keys:
"type" (string, must be either "blog" or "article"), "title" (string, the real title of the article), "description" (string, max 100 characters summary), "category" (string), "date" (string, format like "21 Apr 2026"), "url" (string, a valid working URL to the real article).
Do not include any markdown formatting like \`\`\`json or \`\`\`. Just return the raw JSON array. Make sure the URLs are real and working.`;

        const requestBody = JSON.stringify({
            contents: [{
                parts: [{ text: prompt }]
            }],
            tools: [{ googleSearch: {} }]
        });

        const response = await postJson(GEMINI_API_URL, {
            headers: {
                "Content-Type": "application/json"
            },
            body: requestBody
        });

        if (!response.ok) {
            console.error("Gemini API Error:", response.rawBody);
            return res.status(500).json({ message: "Failed to fetch blogs from AI" });
        }

        const candidateText = response.json?.candidates?.[0]?.content?.parts?.[0]?.text;
        
        let blogs = [];
        if (candidateText) {
            try {
                // Strip markdown formatting if the model still included it
                const cleanedText = candidateText.replace(/```json\n/g, '').replace(/```/g, '').trim();
                blogs = JSON.parse(cleanedText);
            } catch (err) {
                console.error("Failed to parse Gemini JSON:", candidateText);
                blogs = [];
            }
        }

        if (!Array.isArray(blogs) || blogs.length === 0) {
            blogs = [
                {
                    type: "blog",
                    title: "How to Stay Safe While Traveling Alone",
                    description: "Simple tips and precautions every woman should know.",
                    category: "Safety Tips",
                    date: "21 Apr 2026",
                    url: "https://www.nomadicmatt.com/travel-blogs/solo-female-travel-safety/"
                },
                {
                    type: "article",
                    title: "Understanding Your Legal Rights",
                    description: "Know your rights and the laws that protect you.",
                    category: "Legal Awareness",
                    date: "19 Apr 2026",
                    url: "https://www.unwomen.org/en/what-we-do/ending-violence-against-women"
                },
                {
                    type: "article",
                    title: "Building a Supportive Community",
                    description: "The power of women supporting women.",
                    category: "Community",
                    date: "18 Apr 2026",
                    url: "https://leanin.org/circles"
                }
            ];
        }

        return res.json({ blogs });
    } catch (err) {
        console.error("Community Controller Error:", err.message || err);
        // Fallback to static blogs if API completely fails
        return res.json({
            blogs: [
                {
                    type: "blog",
                    title: "How to Stay Safe While Traveling Alone",
                    description: "Simple tips and precautions every woman should know.",
                    category: "Safety Tips",
                    date: "21 Apr 2026",
                    url: "https://www.nomadicmatt.com/travel-blogs/solo-female-travel-safety/"
                },
                {
                    type: "article",
                    title: "Understanding Your Legal Rights",
                    description: "Know your rights and the laws that protect you.",
                    category: "Legal Awareness",
                    date: "19 Apr 2026",
                    url: "https://www.unwomen.org/en/what-we-do/ending-violence-against-women"
                },
                {
                    type: "article",
                    title: "Building a Supportive Community",
                    description: "The power of women supporting women.",
                    category: "Community",
                    date: "18 Apr 2026",
                    url: "https://leanin.org/circles"
                }
            ]
        });
    }
};

exports.createStory = async (req, res) => {
    try {
        const { title, snippet, anonymous } = req.body;
        if (!title || !snippet) {
            return res.status(400).json({ message: "Title and story content are required." });
        }

        const story = await Story.create({
            userId: req.user,
            title,
            snippet,
            anonymous: anonymous || false
        });

        return res.status(201).json({ story });
    } catch (err) {
        console.error("Failed to create story:", err);
        return res.status(500).json({ message: "Failed to share story." });
    }
};

exports.getStories = async (req, res) => {
    try {
        const stories = await Story.find()
            .populate("userId", "name")
            .sort({ createdAt: -1 })
            .limit(50); // Get latest 50 stories
            
        return res.json({ stories });
    } catch (err) {
        console.error("Failed to fetch stories:", err);
        return res.status(500).json({ message: "Failed to fetch stories." });
    }
};

exports.toggleLike = async (req, res) => {
    try {
        const { id } = req.params;
        const story = await Story.findById(id);
        
        if (!story) {
            return res.status(404).json({ message: "Story not found." });
        }

        const userIdStr = req.user.toString();
        const likeIndex = story.likes.findIndex(likeId => likeId.toString() === userIdStr);

        if (likeIndex === -1) {
            // Not liked yet, so add like
            story.likes.push(req.user);
        } else {
            // Already liked, so remove like
            story.likes.splice(likeIndex, 1);
        }

        await story.save();
        return res.json({ likes: story.likes.length, isLiked: likeIndex === -1 });
    } catch (err) {
        console.error("Failed to toggle like:", err);
        return res.status(500).json({ message: "Failed to update like status." });
    }
};
