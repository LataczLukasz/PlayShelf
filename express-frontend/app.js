const express = require('express');
const path = require('path');
const httpErrors = require('http-errors');
const cookieParser = require('cookie-parser');

const app = express();

app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'pug');

app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());

app.use(express.static(path.join(__dirname, 'public')));

app.use((req, res, next) => {
    res.locals.isLoggedIn = !!req.cookies.auth_token;
    if (res.locals.isLoggedIn && (req.path === '/login' || req.path === '/register')) {
        return res.redirect('/games');
    }
    next();
});

const gamesRouter = require('./routes/games');
const authRouter = require('./routes/auth');

app.use('/', authRouter);
app.use('/games', gamesRouter);

app.use((req, res, next) => {
    next(httpErrors(404));
});

app.use((err, req, res, next) => {
    res.locals.message = err.message;
    res.locals.error = req.app.get('env') === 'development' ? err : {};

    res.status(err.status || 500);
    res.render('error');
});

module.exports = app;