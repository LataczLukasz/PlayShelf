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
        res.render('games', {
            title: "Lista gier",
            games
        });
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
        const response = await axios.post(`${serverURL}/games/review/add/`, { rating, review_text, game_id }, {
            headers: {
                'Accept': 'application/json',
                Authorization: `Bearer ${authToken}`
            }
        });
    } catch (error) {
        console.error("Wystąpił błąd");
    }
    res.redirect(`/games/rating/${game_id}`);
};

exports.addToWishlist = async (req, res) => {
    const authToken = req.cookies.auth_token;
    const { id } = req.params;
    try {
        const response = await axios.post(`${serverURL}/games/addToWishlist/add/`, { id }, {
            headers: {
                'Accept': 'application/json',
                Authorization: `Bearer ${authToken}`
            }
        });
        res.status(200).json({ message: response.data.message });
    } catch (error) {
        res.status(500).json({ message: "Wystąpił błąd podczas dodawania gry do listy życzeń." });
    }
};

exports.getWishlist = async (req, res) => {
    const authToken = req.cookies.auth_token;
    try {
        const response = await axios.get(`${serverURL}/games/getWishlist/`, {
            headers: {
                'Accept': 'application/json',
                Authorization: `Bearer ${authToken}`
            }
        });
        const games = response.data.wishlist;
        res.render('wishlist', { games });
    } catch (error) {
        console.error('Błąd podczas pobierania szczegółów gry:', error);
        res.status(500).send('Wystąpił błąd podczas pobierania szczegółów gry.');
    }
};

exports.gameWishlistRemove = async (req, res) => {
    const authToken = req.cookies.auth_token;
    const { id } = req.params;
    try {
        const response = await axios.post(`${serverURL}/games/gameWishlistRemove/`,{id}, {
            headers: {
                'Accept': 'application/json',
                Authorization: `Bearer ${authToken}`
            }
        });
        res.status(200).json({ message: response.data.message });
    } catch (error) {
        res.status(500).json({ message: "Błąd podczas usuwania gry z listy życzeń." });
    }
};