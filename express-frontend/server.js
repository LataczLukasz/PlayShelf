const express = require('express');
const axios = require('axios');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;
const serverURL = "127.0.0.1:8000"
app.use(express.urlencoded({ extended: true }));
// Ustaw Pug jako silnik szablonów
app.set('view engine', 'pug');
app.set('views', path.join(__dirname, 'views'));

// Strona główna
app.get('/', async (req, res) => {
    try {
        const response = await axios.get('http://127.0.0.1:8000/games/', {
            headers: {
                'Accept': 'application/json',
            }
        });
        const games = response.data.games;
        res.render('index', { games });
    } catch (error) {
        console.error('Błąd podczas pobierania gier:', error);
        res.status(500).send('Wystąpił błąd podczas pobierania gier.');
    }
});

app.get('/login', (req, res) => {
    res.render('login');
});

app.post('/login', async (req, res) => {
    const { email, password } = req.body;
    try {
      const loginURL = `http://${serverURL}/api/login/`;
      const response = await axios.post(loginURL, { email, password });
      if (response.status === 200 && response.data.access_token) {
        res.cookie('auth_token', response.data.access_token, { 
          httpOnly: true,
          secure: process.env.NODE_ENV === 'production',
          maxAge: 7 * 24 * 60 * 60 * 1000
        });
        res.redirect('/');
      } else {
        const errorMessage = response.data.error || 'Nieoczekiwana odpowiedź serwera.';
        res.render('login', { 
          error: errorMessage, 
          success: null 
        });
      }
    } catch (error) {
      let errorMessage = 'Wystąpił błąd podczas logowania.';

      res.render('login', { 
        error: errorMessage, 
        success: null 
      });
    }
});

app.get('/register', (req, res) => {
    res.render('register');
});

app.post('/register', async (req, res) => {
    const { email, password, username } = req.body;
    try {
      const loginURL = `http://${serverURL}/api/register/`;
      const response = await axios.post(loginURL, { email, password, username });
      if (response.status === 201) {
        res.redirect('/login');
      } else {
        const errorMessage = response.data.error || 'Nieoczekiwana odpowiedź serwera.';
        res.render('register', { 
          error: errorMessage, 
          success: null 
        });
      }
    } catch (error) {
      let errorMessage = 'Wystąpił błąd podczas rejestracji.';

      res.render('register', { 
        error: errorMessage, 
        success: null 
      });
    }
});


app.listen(PORT, () => {
    console.log(`Serwer działa na http://localhost:${PORT}`);
});
