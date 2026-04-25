const express = require("express");
const cors = require("cors");
require("dotenv").config();

const connectDB = require("./config/db");

const app = express();

connectDB();

app.use(cors());
app.use(express.json());

app.use("/api/auth", require("./routes/authRoutes"));
app.use("/api/users", require("./routes/userRoutes"));
app.use("/api/volunteers", require("./routes/volunteerRoutes"));
app.use("/api/help-requests", require("./routes/helpRequestRoutes"));
app.use("/api/sos", require("./routes/sosRoutes"));
app.use("/api/posts", require("./routes/postRoutes"));
app.use("/api/chatbot", require("./routes/chatbotRoutes"));

const port = process.env.PORT || 5000;
app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});
