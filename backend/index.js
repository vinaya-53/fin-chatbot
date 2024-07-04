const express = require('express');
const cors = require('cors');
const app = express();

const corsOptions = {
    origin: ['https://finance-chatbot-sigma.vercel.app', 'https://finance-chatbot-brkhq2nsf-neptos-projects-a4a06739.vercel.app'],
    optionsSuccessStatus: 200
};

app.use(cors(corsOptions));
app.use(express.json());

app.use("/", (req, res) => {
    res.send("server is running");
});

app.listen(5000, () => {
    console.log("server started on PORT 5000");
});
