const express=require('express')
const app=express()
app.use("/",(req,res)=>{
    res.send("server is running");
});
app.listen(500,console.log("server started on PORT 5000"));