import express from "express";
import cors from "cors";
import fetch from "node-fetch";

const app = express();
app.use(cors());
app.use(express.json());

// Route that forwards the text to your Python Flask API
app.post("/analyze", async (req, res) => {
    const { text } = req.body;

    try {
        const response = await fetch("http://127.0.0.1:5000/analyze", {
            method: "POST", 
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text }),
        });

        const data = await response.json();
        return res.json(data);
    } catch (error) {
        console.error("Error forwarding to Python service:", error);
        return res.status(500).json( {error: "Python API unreachable"} );
    }
});

const PORT = 8000;
app.listen(PORT, () => {
    console.log('Node backend running on port ${PORT}');
})