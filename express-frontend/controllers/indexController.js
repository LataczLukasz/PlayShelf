exports.index = (req, res) => {
    const authToken = req.cookies.auth_token;
    if(authToken)
    {
        res.redirect('games')
    } else {
        res.redirect('login')
    }
    // res.render('index', {
    //     title: 'Strona główna'
    // });
};