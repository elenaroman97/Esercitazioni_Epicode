import pandas as pd
from matplotlib import pyplot as plt

# Caricamento del Dataset
url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
data = pd.read_csv(url)

# Ispeziona il Dataset
print(data.info())
print(data.head())

#### Step 2: Verifica del Dataset e dei rispettivi Metadata

print(data.shape)
print(data.columns)

#### Step 3: Calcolo del numero totale di casi Covid avvenuti in quello stesso continente

# Rimozione di eventuali locazioni che nel Dataset non appartengono ad alcun continente
data = data.dropna(subset=['continent'])

# Calcolo del numero totale di casi per continente
continent_cases = data.groupby('continent')['total_cases'].sum().reset_index()
print(continent_cases)

#### Step 4: Calcolo del numero massimo, della media e della percentuale di casi totali

world_total_cases = data['total_cases'].sum()
continent_stats = data.groupby('continent')['total_cases'].agg(['max', 'median']).reset_index()

# Verifica che non vi siano divisioni per zero
continent_stats['percentage_of_world_total'] = (continent_stats['max'] / world_total_cases) * 100
print(continent_stats)

#### Step 5: Analisi dei dati per quanto riguarda l'Italia nel 2022

# Filtraggio dei dati per quanto riguarda l'Italia 
italy_2022 = data[(data['location'] == 'Italy') & (data['date'].str.contains('2022'))]

# Andamento dei casi totali
plt.figure(figsize=(10, 6))
plt.plot(italy_2022['date'], italy_2022['total_cases'])
plt.title('Italy Total Cases in 2022')
plt.xlabel('Date')
plt.ylabel('Total Cases')
plt.xticks(rotation=45)
plt.show()

# Calcolo e analisi dei nuovi casi nel 2022
new_cases_italy_2022 = italy_2022['new_cases'].sum()

plt.figure(figsize=(6, 6))
plt.bar(['New Cases in 2022'], [new_cases_italy_2022])
plt.title('Italy New Cases in 2022')
plt.ylabel('New Cases')
plt.show()

#### Step 6: Analisi per quanto riguarda la terapia intensiva (Italia , Germania , Francia)

# Dati riguardanti il numero di pazienti in terapia intensiva da Maggio 2022 ad Aprile 2023
icu_data = data[(data['location'].isin(['Italy', 'Germany', 'France'])) &
                (data['date'] >= '2022-05-01') & (data['date'] <= '2023-04-30')]

# Realizzazione del grafico statistico (boxplot) per quanto riguarda le variabili comulative dei casi
plt.figure(figsize=(10, 6))
icu_data.boxplot(column='icu_patients', by='location', grid=False)
plt.title('ICU Patients from May 2022 to April 2023')
plt.suptitle('')
plt.xlabel('Location')
plt.ylabel('ICU Patients')
plt.show()

# Descrizione dei dati trovati
print(icu_data.groupby('location')['icu_patients'].describe())

#### Step 7: Analisi dei pazienti ospedalizzati (Italia, Germania , Francia, Spagna  - 2023)

# Filtraggio dei dati per i pazienti ospedalizzati nel 2023
hosp_data = data[(data['location'].isin(['Italy', 'Germany', 'France', 'Spain'])) &
                 (data['date'].str.contains('2023'))]

# Somma totale dei pazienti ospedalizzati
hosp_sum = hosp_data.groupby('location')['hosp_patients'].sum().reset_index()
print(hosp_sum)
