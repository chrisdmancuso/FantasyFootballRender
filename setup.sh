mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"your-email@domain.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[theme]
primaryColor=’#631284’\n\
backgroundColor=’#000548’\n\
secondaryBackgroundColor=’#123284’\n\
textColor="#DDD"\n\
font = ‘sans serif’\n\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
" > ~/.streamlit/config.toml