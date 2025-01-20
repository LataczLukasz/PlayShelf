const express = require('express');
const axios = require('axios');
const path = require('path');
var cookieParser = require('cookie-parser');
const app = express();
const PORT = process.env.PORT || 3000;
const serverURL = "http://127.0.0.1:8000"
app.use(cookieParser());
app.use(express.urlencoded({ extended: true }));
// Ustaw Pug jako silnik szablonów
app.set('view engine', 'pug');
app.set('views', path.join(__dirname, 'views'));

// Strona główna
app.get('/', async (req, res) => {
  const authToken = req.cookies.auth_token;
    try {
        const response = await axios.get(`${serverURL}/games/`, {
            headers: {
                'Accept': 'application/json',
                Authorization: `Bearer ${authToken}`
            }
        });
        const games = response.data.games;
        res.render('index', { games });
    } catch (error) {
        console.error('Błąd podczas pobierania gier:', error);
        res.status(500).send('Wystąpił błąd podczas pobierania gier.');
    }
});

app.get('/rating/:id', async (req, res) => {
  const authToken = req.cookies.auth_token;
  const { id } = req.params;
    try {
        const response = await axios.get(`${serverURL}/rating/${id}`, {
            headers: {
                'Accept': 'application/json',
                Authorization: `Bearer ${authToken}`
            }
        });
        const reviews = response.data.reviews;
        const myReviews = response.data.my_review;
        const game = response.data.game;
        const game_id = response.data.game_id;
        res.render('rating', { reviews, game, myReviews, game_id });
    } catch (error) {
        console.error('Błąd podczas pobierania gier:', error);
        res.status(500).send('Wystąpił błąd podczas pobierania gier.');
    }
});

app.post('/rating/add', async (req, res) => {
  const authToken = req.cookies.auth_token;
  const { rating, review_text, game_id } = req.body;
  try {
    const response = await axios.post(`${serverURL}/games/review/add/`, { rating, review_text, game_id },
      {
        headers: {
          'Accept': 'application/json',
          Authorization: `Bearer ${authToken}`
        }
      }
    );
    
    if (response.status === 200) {
      console.log("Dodano")
    }else{
      console.log("Nie dodano")
    }
  } catch (error) {
    console.log("Wystapil blad")
  }
  res.redirect(`/rating/${game_id}`)
});


app.get('/login', (req, res) => {
    res.render('login');
});

app.post('/login', async (req, res) => {
    const { email, password } = req.body;
    try {
      const loginURL = `${serverURL}/api/login/`;
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
      const loginURL = `${serverURL}/api/register/`;
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
