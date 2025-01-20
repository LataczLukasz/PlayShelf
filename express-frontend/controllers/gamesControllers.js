const axios = require('axios');

exports.getGames = async (req, res) => {
    try {
        const response = await axios.get('http://127.0.0.1:8000/games/', {
            headers: {
                Accept: 'application/json'
            }
        });
    
        console.log('Odpowiedź z API:', response.data); // Możesz sprawdzić, co zwraca API
        const games = response.data.games; // To prawidłowe, ponieważ API zwraca obiekt 'games'
        
        res.render('games', { 
            title: "Lista gier",
            games
        });
    } catch (error) {
        console.error('Błąd podczas pobierania danych:', error);
        if (error.response) {
            console.error('Szczegóły błędu odpowiedzi:', error.response.data);
            console.error('Status błędu:', error.response.status);
        }
        res.status(500).send('Wystąpił błąd podczas pobierania danych z API.');
    }
};
