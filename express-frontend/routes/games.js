const { Router } = require('express');
const gamesController = require('../controllers/gamesControllers');

const router = Router();

router.get('/', gamesController.getGames);
router.get('/rating/:id', gamesController.getRating);
router.post('/rating/add', gamesController.addRating);

module.exports = router;