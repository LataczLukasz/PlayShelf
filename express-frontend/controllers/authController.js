const axios = require('axios');
const serverURL = 'http://127.0.0.1:8000'; // Zmień na swój URL

exports.login = async (req, res) => {
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
            res.render('login', { error: errorMessage, success: null });
        }
    } catch (error) {
        let errorMessage = 'Wystąpił błąd podczas logowania.';
        res.render('login', { error: errorMessage, success: null });
    }
};

exports.register = async (req, res) => {
    const { email, password, username } = req.body;
    try {
        const registerURL = `${serverURL}/api/register/`;
        const response = await axios.post(registerURL, { email, password, username });
        if (response.status === 201) {
            res.redirect('/login');
        } else {
            const errorMessage = response.data.error || 'Nieoczekiwana odpowiedź serwera.';
            res.render('register', { error: errorMessage, success: null });
        }
    } catch (error) {
        let errorMessage = 'Wystąpił błąd podczas rejestracji.';
        res.render('register', { error: errorMessage, success: null });
    }
};