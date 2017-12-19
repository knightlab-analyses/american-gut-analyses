# copy latest version of otu_trading_cards.tex to each directory then run lualatex
for i in `ls ./latex | egrep "^card_"`
do
	cd ./latex/${i}
	cp ../otu_trading_card_master.tex otu_trading_card.tex
	lualatex otu_trading_card.tex
	cd ../..
done
