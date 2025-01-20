const axios = require('axios');
const serverURL = 'http://127.0.0.1:8000';

exports.getGames = async (req, res) => {
    const authToken = req.cookies.auth_token;
    try {
        const response = await axios.get(`${serverURL}/games/`, {
            headers: {
                'Accept': 'application/json',
                Authorization: `Bearer ${authToken}`
            }
        });
        const games = response.data.games;
        res.render('games', { games });
    } catch (error) {
        console.error('Błąd podczas pobierania gier:', error);
        res.status(500).send('Wystąpił błąd podczas pobierania gier.');
    }
};

exports.getRating = async (req, res) => {
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
        console.error('Błąd podczas pobierania szczegółów gry:', error);
        res.status(500).send('Wystąpił błąd podczas pobierania szczegółów gry.');
    }
};

exports.addRating = async (req, res) => {
    const authToken = req.cookies.auth_token;
    const { rating, review_text, game_id } = req.body;
    try {
        const response = await axios.post(`${serverURL}/games/review/add`, { rating, review_text, game_id }, {
            headers: {
                'Accept': 'application/json',
                Authorization: `Bearer ${authToken}`
            }
        });
        if (response.status === 200) {
            console.log("Dodano");
        } else {
            console.log("Nie dodano");
        }
    } catch (error) {
        console.log("Wystąpił błąd");
    }
    res.redirect(`/rating/${game_id}`);
};