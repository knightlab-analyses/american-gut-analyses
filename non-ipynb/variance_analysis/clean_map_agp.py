#!/usr/bin/env python
import click

import pandas as pd
import numpy as np

from os import mkdir
from os.path import basename, join
from functools import partial


# discard all columns that we cannot process
# ignoring: 'free text', nan, 'datetime: MM/DD/YYYY HH:MM', 'datetime'
DATA_TYPES_TO_PROCESS = ('str', 'bool', 'int', 'string', 'float',
                         'datetime: YYYY', 'datetime: MM/DD/YYYY', 'datetime')
DATA_TYPES_NUMERIC = ('int', 'float')


# Thu, Jun 29, 2017 at 10:40 AM, don't use bmi, age, height or weight
COLS_FOR_FINAL = [
    'bmi_corrected',
    #
    'center_project_name', 'processing_robot', 'primer_plate',
    'extraction_robot', 'plating', 'collection_month', 'vioscreen_vitd2',
    'vioscreen_daidzein', 'high_fat_red_meat_frequency',
    'consume_animal_products_abx', 'meat_eggs_frequency', 'diet_type',
    'vioscreen_hei2010__sea_foods__plant_protiens',
    'vioscreen_hei2010__protien__foods', 'vioscreen_hei2010__sodium',
    'vioscreen_a_bev', 'alcohol_consumption', 'sleep_duration', 'asd',
    'chickenpox', 'level_of_education', 'height_cm', 'age_cat', 'bmi_cat',
    'weight_corrected', 'collection_date', 'elevation', 'last_travel',
    'latitude', 'longitude', 'artificial_sweeteners', 'exercise_frequency',
    'exercise_location', 'olive_oil', 'vioscreen_hei__oils', 'collection_time',
    'fermented_plant_frequency', 'vioscreen_sucpoly',
    'homecooked_meals_frequency', 'prepared_meals_frequency',
    'sugar_sweetened_drink_frequency', 'ready_to_eat_meals_frequency',
    'vioscreen_hei2010__refined__grains', 'vioscreen_fried_fish_servings',
    'vioscreen_fried_food_servings', 'vioscreen_multi_calcium_avg',
    'vioscreen_calcium_avg',
    'allergic_to_i_have_no_food_allergies_that_i_know_of',
    'allergic_to_shellfish', 'allergic_to_peanuts', 'probiotic_frequency',
    'other_supplement_frequency', 'multivitamin',
    'specialized_diet_other_restrictions_not_described_here',
    'drinks_per_session',
    'specialized_diet_westenprice_or_other_lowgrain_low_processed_fo',
    'sugary_sweets_frequency', 'specialized_diet_exclude_refined_sugars',
    'frozen_dessert_frequency', 'salted_snacks_frequency',
    'milk_cheese_frequency', 'lactose', 'milk_substitute_frequency', 'gluten',
    'specialized_diet_modified_paleo_diet', 'fungal_overgrowth', 'sibo',
    'census_region', 'country', 'mental_illness_type_depression',
    'specialized_diet_paleodiet_or_primal_diet',
    'mental_illness_type_anorexia_nervosa',
    'mental_illness_type_bulimia_nervosa', 'vivid_dreams',
    'mental_illness_type_ptsd_posttraumatic_stress_disorder',
    'acid_reflux', 'diabetes', 'antibiotic_history', 'cosmetics_frequency',
    'deodorant_use', 'softener', 'contraceptive', 'acne_medication',
    'acne_medication_otc', 'livingwith', 'liver_disease', 'cancer_treatment',
    'pets_other', 'cat', 'dog', 'drinking_water_source', 'cancer',
    'flossing_frequency', 'tonsils_removed', 'appendix_removed',
    'fed_as_infant', 'kidney_disease', 'cardiovascular_disease',
    'flu_vaccine_date', 'pregnant', 'weight_change', 'alcohol_types_red_wine',
    'alcohol_types_white_wine', 'breastmilk_formula_ensure',
    'teethbrushing_frequency', 'dominant_hand',
    'epilepsy_or_seizure_disorder', 'add_adhd',
    'mental_illness_type_bipolar_disorder', 'smoking_frequency',
    'alcohol_types_beercider', 'alcohol_types_sour_beers', 'nail_biter',
    'pool_frequency', 'csection', 'race', 'last_move',
    'alcohol_types_spiritshard_alcohol', 'roommates', 'lung_disease',
    'non_food_allergies_pet_dander', 'seasonal_allergies',
    'non_food_allergies_drug_eg_penicillin',
    'non_food_allergies_poison_ivyoak', 'non_food_allergies_beestings',
    'well_id', 'non_food_allergies_sun', 'skin_condition', 'migraine', 'ibs',
    'mental_illness', 'cdiff', 'autoimmune', 'clinical_condition', 'ibd',
    'bowel_movement_frequency', 'bowel_movement_quality',
    'vioscreen_hei2010__empty__calories', 'vioscreen_d_cheese',
    'vioscreen_tfa181t', 'vioscreen_clac9t11', 'seafood_frequency',
    'vioscreen_m_fish_hi', 'vioscreen_alanine', 'vioscreen_m_frank',
    'vioscreen_m_meat', 'vioscreen_m_mpf', 'vioscreen_copper',
    'vioscreen_cholest', 'vioscreen_d_yogurt', 'vioscreen_calcium.1',
    'vioscreen_g_whl', 'vioscreen_add_sug', 'vioscreen_fol_deqv',
    'vioscreen_avcarb', 'vioscreen_inositol', 'vioscreen_f_citmlb',
    'vioscreen_betacryp', 'fruit_frequency', 'vioscreen_erythr',
    'vegetable_frequency', 'vioscreen_lutzeax', 'vioscreen_alphacar',
    'types_of_plants', 'vioscreen_xylitol',
    'vioscreen_salad_vegetable_servings', 'vioscreen_caffeine',
    'one_liter_of_water_a_day_frequency', 'vioscreen_grams',
    'vioscreen_lycopene', 'vioscreen_v_starcy', 'vioscreen_biochana',
    'vioscreen_fiber', 'vioscreen_formontn', 'vioscreen_betatoco',
    'vioscreen_delttoco', 'vioscreen_acesupot', 'vioscreen_alphtoce']

# VIOSCREEN_FIELDS =
# the data type of the vioscreen columns, as described in the pull down
VIOSCREEN_FIELDS = {

    # final
    'exercise_location': 'string',

    # we also need to add the
    # 'center_project_name': 'string', 'run_center': 'string',
    # 'mastermix_lot': 'string',
    'barcode': 'string', 'center_name': 'string',
    'center_project_name': 'string', 'comments_renamed': 'string',
    'condition_renamed': 'string', 'experiment_center': 'string',
    'experiment_design_description': 'string', 'experiment_title': 'string',
    'extraction_robot': 'string', 'extractionkit_lot': 'string',
    'instrument_model': 'string', 'library_construction_protocol': 'string',
    'linker': 'string', 'mastermix_lot': 'string', 'pcr_primers': 'string',
    'plateid': 'string', 'platform': 'string', 'plating': 'string',
    'primer': 'string', 'primer_date': 'string', 'primer_plate': 'string',
    'primerplate_renamed': 'string', 'processing_robot': 'string',
    'project_name': 'string', 'qiita_prep_id': 'string',
    'run_center': 'string', 'run_date': 'string', 'run_prefix': 'string',
    'samp_size': 'string', 'sample_center': 'string', 'sample_plate': 'string',
    'sequencing_meth': 'string', 'target_gene': 'string',
    'target_subfragment': 'string', 'tm1000_8_tool': 'string',
    'tm300_8_tool': 'string', 'tm50_8_tool': 'string', 'water_lot': 'string',
    'well': 'string', 'well_id': 'string',
    # actual VIOSCREEN_FIELDS
    # added for final
    'vioscreen_calcium.1': 'float',
    # original
    'vioscreen_a_bev': 'float', 'vioscreen_a_cal': 'float',
    'vioscreen_acesupot': 'float', 'vioscreen_add_sug': 'float',
    'vioscreen_addsugar': 'float', 'vioscreen_adsugtot': 'float',
    'vioscreen_alanine': 'float', 'vioscreen_alcohol': 'float',
    'vioscreen_alcohol_servings': 'float', 'vioscreen_alphacar': 'float',
    'vioscreen_alphtoce': 'float', 'vioscreen_alphtoco': 'float',
    'vioscreen_arginine': 'float', 'vioscreen_ash': 'float',
    'vioscreen_aspartam': 'float', 'vioscreen_aspartic': 'float',
    'vioscreen_avcarb': 'float', 'vioscreen_betacar': 'float',
    'vioscreen_betacryp': 'float', 'vioscreen_betaine': 'float',
    'vioscreen_betatoco': 'float', 'vioscreen_biochana': 'float',
    'vioscreen_caffeine': 'float', 'vioscreen_calcium': 'float',
    'vioscreen_calcium_avg': 'int', 'vioscreen_calcium_dose': 'int',
    'vioscreen_calcium_freq': 'str',
    'vioscreen_calcium_from_dairy_servings': 'float',
    'vioscreen_calcium_servings': 'float',
    'vioscreen_calories': 'float', 'vioscreen_carbo': 'float',
    'vioscreen_cholest': 'float', 'vioscreen_choline': 'float',
    'vioscreen_clac9t11': 'float', 'vioscreen_clat10c12': 'float',
    'vioscreen_copper': 'float', 'vioscreen_coumest': 'float',
    'vioscreen_cystine': 'float', 'vioscreen_d_cheese': 'float',
    'vioscreen_d_milk': 'float', 'vioscreen_d_tot_soym': 'float',
    'vioscreen_d_total': 'float', 'vioscreen_d_yogurt': 'float',
    'vioscreen_daidzein': 'float', 'vioscreen_delttoco': 'float',
    'vioscreen_discfat_oil': 'float', 'vioscreen_discfat_sol': 'float',
    'vioscreen_erythr': 'float', 'vioscreen_f_citmlb': 'float',
    'vioscreen_f_nj_citmlb': 'float', 'vioscreen_f_nj_other': 'float',
    'vioscreen_f_nj_total': 'float', 'vioscreen_f_other': 'float',
    'vioscreen_f_total': 'float', 'vioscreen_fat': 'float',
    'vioscreen_fiber': 'float', 'vioscreen_fibh2o': 'float',
    'vioscreen_fibinso': 'float', 'vioscreen_fish_servings': 'float',
    'vioscreen_fol_deqv': 'float', 'vioscreen_fol_nat': 'float',
    'vioscreen_fol_syn': 'float', 'vioscreen_formontn': 'float',
    'vioscreen_fried_fish_servings': 'float',
    'vioscreen_fried_food_servings': 'float', 'vioscreen_frt5_day': 'float',
    'vioscreen_frtsumm': 'float', 'vioscreen_fructose': 'float',
    'vioscreen_fruit_servings': 'float', 'vioscreen_g_nwhl': 'float',
    'vioscreen_g_total': 'float', 'vioscreen_g_whl': 'float',
    'vioscreen_galactos': 'float', 'vioscreen_gammtoco': 'float',
    'vioscreen_genistn': 'float', 'vioscreen_glac': 'float',
    'vioscreen_gltc': 'float', 'vioscreen_glucose': 'float',
    'vioscreen_glutamic': 'float', 'vioscreen_glycine': 'float',
    'vioscreen_glycitn': 'float', 'vioscreen_grams': 'float',
    'vioscreen_hei2010__dairy': 'float',
    'vioscreen_hei2010__empty__calories': 'float',
    'vioscreen_hei2010__fatty__acids': 'float',
    'vioscreen_hei2010__fruit': 'float',
    'vioscreen_hei2010__greens__beans': 'float',
    'vioscreen_hei2010__protien__foods': 'float',
    'vioscreen_hei2010__refined__grains': 'float',
    'vioscreen_hei2010__sea_foods__plant_protiens': 'float',
    'vioscreen_hei2010__sodium': 'float', 'vioscreen_hei2010__veg': 'float',
    'vioscreen_hei2010__whole__fruit': 'float',
    'vioscreen_hei2010__whole__grains': 'float',
    'vioscreen_hei2010_score': 'float',
    'vioscreen_hei__drk_g__org_veg__leg': 'float',
    'vioscreen_hei__fruit': 'float', 'vioscreen_hei__grains': 'float',
    'vioscreen_hei__meat__beans': 'float', 'vioscreen_hei__milk': 'float',
    'vioscreen_hei__non_juice_frt': 'float', 'vioscreen_hei__oils': 'float',
    'vioscreen_hei__sat_fat': 'float', 'vioscreen_hei__sodium': 'float',
    'vioscreen_hei__sol_fat__alc__add_sug': 'float',
    'vioscreen_hei__veg': 'float', 'vioscreen_hei__whl__grains': 'float',
    'vioscreen_hei_score': 'float', 'vioscreen_histidin': 'float',
    'vioscreen_inositol': 'float', 'vioscreen_iron': 'float',
    'vioscreen_isoleuc': 'float', 'vioscreen_isomalt': 'float',
    'vioscreen_joules': 'float', 'vioscreen_juice_servings': 'float',
    'vioscreen_lactitol': 'float', 'vioscreen_lactose': 'float',
    'vioscreen_legumes': 'float', 'vioscreen_leucine': 'float',
    'vioscreen_line_gi': 'float', 'vioscreen_low_fat_dairy_serving': 'float',
    'vioscreen_lutzeax': 'float', 'vioscreen_lycopene': 'float',
    'vioscreen_lysine': 'float', 'vioscreen_m_egg': 'float',
    'vioscreen_m_fish_hi': 'float', 'vioscreen_m_fish_lo': 'float',
    'vioscreen_m_frank': 'float', 'vioscreen_m_meat': 'float',
    'vioscreen_m_mpf': 'float', 'vioscreen_m_nutsd': 'float',
    'vioscreen_m_organ': 'float', 'vioscreen_m_poult': 'float',
    'vioscreen_m_soy': 'float', 'vioscreen_magnes': 'float',
    'vioscreen_maltitol': 'float', 'vioscreen_maltose': 'float',
    'vioscreen_mangan': 'float', 'vioscreen_mannitol': 'float',
    'vioscreen_methhis3': 'float', 'vioscreen_methion': 'float',
    'vioscreen_mfa141': 'float', 'vioscreen_mfa161': 'float',
    'vioscreen_mfa181': 'float', 'vioscreen_mfa201': 'float',
    'vioscreen_mfa221': 'float', 'vioscreen_mfatot': 'float',
    'vioscreen_multi_calcium_avg': 'int',
    'vioscreen_multi_calcium_dose': 'int', 'vioscreen_multivitamin': 'bool',
    'vioscreen_multivitamin_freq': 'int', 'vioscreen_natoco': 'float',
    'vioscreen_nccglbr': 'float', 'vioscreen_nccglgr': 'float',
    'vioscreen_niacin': 'float', 'vioscreen_niacineq': 'float',
    'vioscreen_nitrogen': 'float',
    'vioscreen_non_fried_fish_servings': 'float', 'vioscreen_omega3': 'float',
    'vioscreen_oxalic': 'float', 'vioscreen_oxalicm': 'float',
    'vioscreen_pantothe': 'float', 'vioscreen_pectins': 'float',
    'vioscreen_pfa182': 'float', 'vioscreen_pfa183': 'float',
    'vioscreen_pfa184': 'float', 'vioscreen_pfa204': 'float',
    'vioscreen_pfa205': 'float', 'vioscreen_pfa225': 'float',
    'vioscreen_pfa226': 'float', 'vioscreen_pfatot': 'float',
    'vioscreen_phenylal': 'float', 'vioscreen_phosphor': 'float',
    'vioscreen_phytic': 'float', 'vioscreen_pinitol': 'float',
    'vioscreen_potass': 'float', 'vioscreen_proline': 'float',
    'vioscreen_protanim': 'float', 'vioscreen_protein': 'float',
    'vioscreen_protveg': 'float', 'vioscreen_questionnaire': 'str',
    'vioscreen_retinol': 'float', 'vioscreen_rgrain': 'float',
    'vioscreen_ribofla': 'float', 'vioscreen_sacchar': 'float',
    'vioscreen_salad_vegetable_servings': 'float', 'vioscreen_satoco': 'float',
    'vioscreen_selenium': 'float', 'vioscreen_serine': 'float',
    'vioscreen_sfa100': 'float', 'vioscreen_sfa120': 'float',
    'vioscreen_sfa140': 'float', 'vioscreen_sfa160': 'float',
    'vioscreen_sfa170': 'float', 'vioscreen_sfa180': 'float',
    'vioscreen_sfa200': 'float', 'vioscreen_sfa220': 'float',
    'vioscreen_sfa40': 'float', 'vioscreen_sfa60': 'float',
    'vioscreen_sfa80': 'float', 'vioscreen_sfatot': 'float',
    'vioscreen_sodium': 'float', 'vioscreen_sorbitol': 'float',
    'vioscreen_starch': 'float', 'vioscreen_sucpoly': 'float',
    'vioscreen_sucrlose': 'float', 'vioscreen_sucrose': 'float',
    'vioscreen_sweet_servings': 'float', 'vioscreen_tagatose': 'float',
    'vioscreen_tfa161t': 'float', 'vioscreen_tfa181t': 'float',
    'vioscreen_tfa182t': 'float', 'vioscreen_tgrain': 'float',
    'vioscreen_thiamin': 'float', 'vioscreen_threonin': 'float',
    'vioscreen_totaltfa': 'float', 'vioscreen_totcla': 'float',
    'vioscreen_totfolat': 'float', 'vioscreen_totsugar': 'float',
    'vioscreen_tryptoph': 'float', 'vioscreen_tyrosine': 'float',
    'vioscreen_username': 'str', 'vioscreen_v_drkgr': 'float',
    'vioscreen_v_orange': 'float', 'vioscreen_v_other': 'float',
    'vioscreen_v_potato': 'float', 'vioscreen_v_starcy': 'float',
    'vioscreen_v_tomato': 'float', 'vioscreen_v_total': 'float',
    'vioscreen_valine': 'float', 'vioscreen_veg5_day': 'float',
    'vioscreen_vegetable_servings': 'float', 'vioscreen_vegsumm': 'float',
    'vioscreen_vita_iu': 'float', 'vioscreen_vita_rae': 'float',
    'vioscreen_vita_re': 'float', 'vioscreen_vitb12': 'float',
    'vioscreen_vitb6': 'float', 'vioscreen_vitc': 'float',
    'vioscreen_vitd': 'float', 'vioscreen_vitd2': 'float',
    'vioscreen_vitd3': 'float', 'vioscreen_vitd_iu': 'float',
    'vioscreen_vite_iu': 'float', 'vioscreen_vitk': 'float',
    'vioscreen_water': 'float', 'vioscreen_wgrain': 'float',
    'vioscreen_whole_grain_servings': 'float', 'vioscreen_xylitol': 'float',
    'vioscreen_zinc': 'float', 'alcohol_frequency': 'string'}


@click.option('--mapping', type=click.File('rb'), help='mapping filepath')
@click.option('--data-dictionary', type=click.File('rb'),
              help='data directory filepath')
@click.option('--output', type=click.Path(exists=False),
              help='output filepath')
@click.command()
def servicio(mapping, data_dictionary, output):
    if mapping is None:
        raise ValueError("You need to pass a mapping")
    if data_dictionary is None:
        raise ValueError("You need to pass a data-dictionary")
    if output is None:
        raise ValueError("You need to pass a output")

    mkdir(output)
    pj = partial(join, output)
    mn = basename(mapping.name)
    quartiles_fp = pj(mn + '.quartiles.tsv')
    deciles_fp = pj(mn + '.deciles.tsv')
    data_dict_fp = pj('data_dictionary.tsv')

    map_ = pd.read_csv(mapping, sep='\t', dtype=str)
    map_.set_index('#SampleID', inplace=True)

    dict_ = pd.read_csv(data_dictionary, sep=',', index_col='column_name')

    # adding extra columns to the data_dictionary
    dict_.loc['height_corrected', 'data type'] = 'int'
    dict_.loc['weight_corrected', 'data type'] = 'int'
    for field, dt in VIOSCREEN_FIELDS.items():
        dict_.loc[field, 'data type'] = dt

    # initial cleaning
    map_.replace(['Unspecified', 'not applicable'], np.nan, inplace=True)
    countries = map_[
        ['country', 'country_of_birth', 'country_residence']].dropna()
    countries.replace('USA', 'United States', inplace=True)

    # We are only interested in the columns in COLS_FOR_FINAL, dropping
    # anything else
    to_remove = set(map_) - set(COLS_FOR_FINAL)
    map_.drop(to_remove, axis='columns', inplace=True)
    map_.replace("Not sure", np.nan, inplace=True)

    # special cases
    replacements = {}
    # Because age and BMI have categories without bounds, we'll set bounds for
    # the categories based on their continous values.
    # For BMI, we'll only look at people with BMIs between 16 and 40.
    map_.loc[
        (map_['bmi_corrected'].astype(float) < 16) |
        (map_['bmi_corrected'].astype(float) > 40), 'bmi_cat'] = np.nan
    map_.drop(['bmi_cat'], axis='columns', inplace=True)
    # map_['bmi'] = np.nan
    # For age, we'll oonly look at people up to the age of 69, so we'll ignore
    # the "70+" category, which is unbounded.
    replacements['age_cat'] = {"70+": np.nan}
    # We dropped people who were uncertain about their stool quality for the
    # comparison, since this was a special category.
    replacements['bowel_movement_quality'] = {
        "I don't know, I do not have a point of reference": np.nan}
    replacements['exercise_location'] = {'None of the above': np.nan}
    # There are also several ordinal categories where the extremes are too
    # small to be analyzed on their own, but could be combined.
    replacements['antibiotic_history'] = {"Week": "Month"}
    replacements['sleep_duration'] = {
        'Less than 5 hours': 'Less than 6', '5-6 hours': 'Less than 6'}
    replacements['bowel_movement_frequency'] = {
        'Four': 'Four or more', 'Five or more': 'Four or more'}
    replacements['diet_type'] = {'Vegan': 'Vegetarian'}
    replacements['last_move'] = {
        'Within the past month': 'Within the past 3 months'}
    replacements['pool_frequency'] = {
        'Occasionally (1-2 times/week)': 'Weekly',
        'Regularly (3-5 times/week)': "Weekly", 'Daily': "Weekly"}
    replacements['smoking_frequency'] = {
        'Occasionally (1-2 times/week)': 'Weekly',
        'Regularly (3-5 times/week)': "Weekly", 'Daily': "Weekly"}
    replacements['sugar_sweetened_drink_frequency'] = {
        'Occasionally (1-2 times/week)': 'Weekly',
        'Regularly (3-5 times/week)': "Weekly", 'Daily': "Weekly"}
    replacements['vivid_dreams'] = {
        'Occasionally (1-2 times/week)': 'Weekly',
        'Regularly (3-5 times/week)': "Weekly", 'Daily': "Weekly"}
    replacements['frozen_dessert_frequency'] = {
        'Occasionally (1-2 times/week)': 'Weekly',
        'Regularly (3-5 times/week)': "Weekly", 'Daily': "Weekly"}
    # We'll also combine vegans and vegetarians into a single category.
    replacements['vegetable_frequency'] = {
        'Never': "Less than weekly",
        'Rarely (less than once/week)': "Less than weekly"}
    map_.replace(replacements, inplace=True)

    # We're going to exclude clincial covariate columns if the individual does
    # not report being diagnosed by a medical professional.
    clincial_correction = {
        'Self-diagnosed': np.nan,
        'Diagnosed by an alternative medicine practitioner': np.nan}
    clinical_replace = {
        col: clincial_correction
        for col in dict_.loc[
            dict_['question_type'] == 'medical condition'].index}
    map_.replace(clinical_replace, inplace=True)

    for column_name in map_.columns.values:
        dt = dict_.loc[column_name]['data type']

    # remove all columns with only NaN
    map_.dropna(axis=1, how='all', inplace=True)

    # generate our new DataFrames
    quartiles = map_.copy(deep=True)
    deciles = map_.copy(deep=True)
    for column_name in map_.columns.values:
        dt = dict_.loc[column_name]['data type']
        if dt in DATA_TYPES_NUMERIC:
            # we need to calculate the bins so we know that nothing else
            # will fail
            quartiles[column_name] = pd.to_numeric(
                quartiles[column_name], errors='coerce')
            deciles[column_name] = pd.to_numeric(
                deciles[column_name], errors='coerce')
            quartiles[column_name], qbins = pd.qcut(
                quartiles[column_name], 4, labels=False, retbins=True,
                duplicates='drop')
            deciles[column_name], dbins = pd.qcut(
                deciles[column_name], 10, labels=False, retbins=True,
                duplicates='drop')

            # confirm that we have the expected number of bins
            if len(qbins) != 5:
                quartiles[column_name] = np.nan
            if len(dbins) != 11:
                deciles[column_name] = np.nan
        elif dt == 'bool':
            if quartiles[column_name].nunique() > 2:
                quartiles[column_name] = quartiles[column_name].map({
                    'False': 'No', 'True': 'Yes'})
            if deciles[column_name].nunique() > 2:
                deciles[column_name] = deciles[column_name].map({
                    'False': 'No', 'True': 'Yes'})

    quartiles.dropna(axis=1, how='all', inplace=True)
    deciles.dropna(axis=1, how='all', inplace=True)

    for column_name in quartiles:
        quartiles[column_name] = _clean_column(quartiles[column_name])
    for column_name in deciles:
        deciles[column_name] = _clean_column(deciles[column_name])
    quartiles.dropna(axis=1, how='all', inplace=True)
    deciles.dropna(axis=1, how='all', inplace=True)

    quartiles.fillna('nan', inplace=True)
    deciles.fillna('nan', inplace=True)

    quartiles.to_csv(quartiles_fp, sep='\t')
    deciles.to_csv(deciles_fp, sep='\t')
    dict_.to_csv(data_dict_fp, sep='\t')


def _clean_column(column):
    # let's check the size of the groups and discard anything that
    # has less than 50 samples or represents under 0.03 of the size
    counts = pd.DataFrame(
        [column.value_counts(),
         column.value_counts(normalize=True)],
        index=['counts', 'perc']).T
    check = (counts['counts'] < 50) | (counts['perc'] < 0.03)
    replace = check.index[check]
    if replace.size != 0:
        column.replace({v: np.nan for v in replace}, inplace=True)
    # there is 2 or more groups
    if column.nunique() == 1:
        column = np.nan
    # # at least 1000 samples have a value
    # try:
    #     if column.count() < 5000:
    #         column = np.nan
    # except:
    #     pass

    return column


if __name__ == '__main__':
    servicio()
