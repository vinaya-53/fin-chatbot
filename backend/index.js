const express = require('express');
const cors = require('cors');
const app = express();

const corsOptions = {
    origin: ['*'],
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
