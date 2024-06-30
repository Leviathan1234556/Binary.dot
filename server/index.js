const express = require("express");
const mongoose = require('mongoose');
const cors = require("cors");
const UserModel = require('./models/users');

const app = express();
app.use(express.json());
app.use(cors({
    origin: ['https://binary-dot-975m.vercel.app/'],
    methods: ['POST', 'GET'],
    credentials: true
}));

mongoose.connect("mongodb://127.0.0.1:27017/Users", {
    useNewUrlParser: true,
    useUnifiedTopology: true,
}).then(() => {
    console.log('Connected to MongoDB');
}).catch(err => console.log(err));

app.get('/users', (req, res) => {
    UserModel.find()
        .then(users => res.json(users))
        .catch(err => res.status(500).json(err));
});

app.post('/login', (req, res) => {
    const { email, password } = req.body;
    UserModel.findOne({ email })
        .then(user => {
            if (user) {
                if (user.password === password) {
                    res.json("Success");
                } else {
                    res.status(401).json("The password is incorrect");
                }
            } else {
                res.status(404).json("No record existed");
            }
        })
        .catch(err => res.status(500).json(err));
});

app.post('/register', (req, res) => {
    UserModel.create(req.body)
        .then(user => res.json(user))
        .catch(err => res.status(500).json(err));
});

app.listen(3001, () => {
    console.log("Server is running on port 3001");
});
