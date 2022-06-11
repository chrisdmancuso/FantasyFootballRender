mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"your-email@domain.com\"\n\
" > ~/.streamlit/credentials.toml

echo "[theme]
primaryColor=’#631284’
backgroundColor=’#000548’
secondaryBackgroundColor=’#123284’
textColor="#DDD"
font = ‘sans serif’
[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml