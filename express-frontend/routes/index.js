const { Router } = require('express');

const router = Router();

router.get('/', (req, res) => {
    if (!res.locals.isLoggedIn) {
        return res.redirect('/login');
    }
    res.render('home');
});

module.exports = router;