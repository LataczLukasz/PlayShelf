const { Router } = require('express');
const gamesController = require('../controllers/gamesControllers');

const router = Router();

router.get('/', gamesController.getGames);

module.exports = router;