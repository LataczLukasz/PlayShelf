const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

app.get('/', (req, res) => {
    res.send('Witamy w aplikacji Express!');
});

app.listen(PORT, () => {
    console.log(`Serwer działa na porcie ${PORT}`);
});