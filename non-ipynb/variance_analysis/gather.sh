echo -e "#rare\tmetric\tcategory\tp\tf\tr2"
for f in `find . -name "adonis_results.txt" -print`
do
    rare=$(echo $f | awk -F'/' '{ print $2 }')
    metric=$(echo $f | awk -F'/' '{ print $3 }')
    category=$(echo $f | awk -F'/' '{ print $4 }')
  
    # for results of the form
    #                                  Df SumsOfSqs MeanSqs F.Model     R2    Pr(>F)
    #qiime.data$map[[opts$category]]    9      3.36 0.37362  8.5531 0.0085 9.999e-05
    #Residuals                       8978    392.18 0.04368         0.9915
    #Total                           8987    395.54                 1.0000

    #qiime.data$map[[opts$category]] ***
    #Residuals
    #Total
    #---
    #Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1
    p_results=$(grep -A 1 "R2 *Pr" $f | grep qiime)
    if [[ "$?" == 0 ]]; then
        p=$(echo $p_results | awk '{ print $7 }')
    else
        # for results of the form
        #                                  Df SumsOfSqs MeanSqs F.Model      R2
        #qiime.data$map[[opts$category]]    5      2.12 0.42347   9.668 0.00535
        #Residuals                       8982    393.43 0.04380         0.99465
        #Total                           8987    395.54                 1.00000
        #                                   Pr(>F)
        #qiime.data$map[[opts$category]] 9.999e-05 ***
        #Residuals
        #Total
        #---
        #Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1
        p_results=$(grep -A 1 "^ *Pr" $f)
        if [[ "$?" == 1 ]]; then
            p='not-reported'
        else
            p=$(echo $p_results | grep qiime | awk '{ print $3 }')
        fi
    fi
    #                                   Df SumsOfSqs MeanSqs F.Model     R2
    #qiime.data$map[[opts$category]]    9      3.36 0.37362  8.5531 0.0085 
    effect_results=$(grep -A 1 "F.Model *R2" $f | grep qiime)
    f=$(echo $effect_results | awk '{ print $5 }')
    r2=$(echo $effect_results | awk '{ print $6 }')

    echo -e "${rare}\t${metric}\t${category}\t${p}\t${f}\t${r2}"
done
