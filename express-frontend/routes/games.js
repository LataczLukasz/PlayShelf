const { Router } = require('express');
const gamesController = require('../controllers/gamesControllers');

const router = Router();

router.get('/', gamesController.getGames);
router.post('/rating/add', gamesController.addRating);
router.get('/rating/:id', gamesController.getRating);
router.get('/addToWishlist/:id', gamesController.addToWishlist);
router.get('/getWishlist', gamesController.getWishlist);
router.get('/gameWishlistRemove/:id', gamesController.gameWishlistRemove);

module.exports = router;