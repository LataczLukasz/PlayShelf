const express = require('express');
const path = require('path');
const httpErrors = require('http-errors');

const app = express();

app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'pug');

app.use(express.urlencoded({ extended: false }));

const indexRouter = require('./routes/index');
const gamesRouter = require('./routes/games');

app.use('/', indexRouter);
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