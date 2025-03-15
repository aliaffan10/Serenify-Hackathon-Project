const express = require("express");
const cors = require("cors");
const { GoogleGenerativeAI } = require("@google/generative-ai");
const fs = require("fs");
const path = require("path");
const axios = require("axios");

const app = express();
const port = 4000;
const genAI = new GoogleGenerativeAI("AIzaSyCBTej4OM9RSAn2TEiIbfFAqAGKD-x2Ae4"); // Replace with your actual API key

const SYSTEM_INSTRUCTION = "You are a compassionate mental health and wellbeing assistant chatbot. Provide empathetic, supportive, and informative responses.";

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, "public")));

// Chatbot API Endpoint
app.post("/chatbot", async (req, res) => {
  const userPrompt = req.body.prompt;

  // Constructing final chatbot prompt with system instruction
  const finalPrompt = `
    <system>
    You are a compassionate mental health and wellbeing chatbot designed to provide support and guidance.
    Your main objective is to create a safe, non-judgmental space for users to discuss their feelings,
    thoughts, and mental health concerns.
    Your response should be no more than 80 words.
    </system>

    <user>
    ${userPrompt}
    </user>
  `;

  console.log("Received prompt:", finalPrompt);

  try {
    // Call Gemini AI with System Instruction
    const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });
    const result = await model.generateContent(finalPrompt);

    console.log("Full API Response:", JSON.stringify(result, null, 2));

    // ✅ Fix: Extracting AI response correctly
    if (
      result.response &&
      result.response.candidates &&
      result.response.candidates.length > 0 &&
      result.response.candidates[0].content &&
      result.response.candidates[0].content.parts.length > 0
    ) {
      const responseText = result.response.candidates[0].content.parts[0].text;
      console.log("AI Response:", responseText);
      res.json({ response: responseText });
    } else {
      console.log("Error: No valid response from AI.");
      res.status(500).json({ error: "No valid response from AI." });
    }
  } catch (error) {
    console.error("Error during API call:", error);
    res.status(500).json({ error: "Something went wrong." });
  }
});

// Analyze Endpoint: For emotion and suicidal risk detection (Forwarding request to Flask)
app.post("/analyze", async (req, res) => {
  try {
    const userMessage = req.body.message;
    if (!userMessage) {
      return res.status(400).json({ error: "No message provided" });
    }
    // Forward the request to Flask's /analyze endpoint
    const flaskResponse = await axios.post("http://127.0.0.1:5000/analyze", { message: userMessage });
    res.json(flaskResponse.data);
  } catch (error) {
    console.error("Error calling Flask /analyze:", error.message);
    res.status(500).json({ error: "Error analyzing message." });
  }
});

// Heatmap Endpoint (Forward request to Flask)
app.get("/heatmap", async (req, res) => {
  try {
    const flaskResponse = await axios.get("http://127.0.0.1:5000/heatmap");
    res.json(flaskResponse.data);
  } catch (error) {
    console.error("Error calling Flask /heatmap:", error.message);
    res.status(500).json({ error: "Error generating heatmap." });
  }
});

app.listen(port, () => {
  console.log(`Server running at http://127.0.0.1:${port}`);
});
