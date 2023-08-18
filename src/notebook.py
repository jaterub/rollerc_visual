#!/usr/bin/env python
# coding: utf-8

# In[122]:


import numpy as np
import os
import matplotlib.pylab as plt
import seaborn as sns
import folium
import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objs as go
import plotly.subplots
import plotly.figure_factory as ff
import plotly.graph_objs as go
pd.set_option('display.max_columns', None)


# In[123]:


# Obtén la ruta del directorio actual
path = os.getcwd()

# Sube un nivel en la estructura de directorios para llegar a la carpeta raíz del proyecto
project_root = os.path.dirname(path)

# Construye la ruta al archivo csv
csv_path = os.path.join(project_root, 'data', 'raw', 'coaster_db.csv')


# In[124]:


df = pd.read_csv(csv_path)
df.head()


# In[125]:


df.shape


# In[126]:


df.describe()


# In[127]:


df.info(5)


# In[128]:


df.columns


# In[129]:


df = df [['coaster_name', 'Location', 'Status', 'Manufacturer',
       'year_introduced', 'latitude', 'longitude', 'Type_Main',
       'opening_date_clean', 'speed1', 'speed2', 'speed1_value', 'speed1_unit',
       'speed_mph', 'height_ft',
       'Inversions_clean', 'Gforce_clean']]
df.head()


# In[130]:


df.info()


# In[131]:


df['opening_date_clean'] = pd.to_datetime(df['opening_date_clean'],errors='coerce')


# In[132]:


df = df.rename(columns={'coaster_name':'Coaster_Name',
                   'year_introduced':'Year_Introduced',
                   'opening_date_clean':'Opening_Date',
                   'speed_mph':'Speed_mph',
                   'height_ft':'Height_ft',
                   'Inversions_clean':'Inversions',
                   'Gforce_clean':'Gforce'})


# In[133]:


# Check for duplicate coaster name
df.loc[df.duplicated(subset=['Coaster_Name'])].head()


# In[134]:


# # Null percentage
# df.loc[:,df.isna().mean() < 0.30]


# In[135]:


# sns.heatmap(df, annot=True)


# In[136]:


# Checking an example duplicate
df.query('Coaster_Name == "American Dreier Looping"')


# In[137]:


df_procesed = df.loc[~df.duplicated(subset=['Coaster_Name','Location','Opening_Date'])].reset_index(drop=True).copy()


# In[138]:


df_procesed.head()


# In[139]:


path = os.getcwd()

project_root = os.path.dirname(path)

csv_path = os.path.join(project_root, 'data', 'processed', 'data_procesed.csv')
df_procesed.to_csv(csv_path, index=False)


# In[140]:


sns.regplot(x=df_procesed['Speed_mph'], y=df_procesed['Height_ft'])


# In[141]:


df_procesed.isna().sum().sum()


# In[142]:


sns.pairplot(df_procesed,
             vars=['Year_Introduced','Speed_mph',
                   'Height_ft','Inversions','Gforce'],
            hue='Type_Main')
plt.show()


# In[143]:


df_procesed.info()


# In[144]:


df_procesed['Type_Main'].unique()


# In[145]:


df_corr = df[['Year_Introduced','Speed_mph','Height_ft','Inversions','Gforce']].dropna().corr()


# In[146]:


sns.heatmap(df_corr, annot=True)


# In[147]:


df_clean = df_procesed.dropna()


# In[148]:


# Crea un gráfico de densidad para la columna 'Speed_mph'
fig = ff.create_distplot([df_clean['Speed_mph']], group_labels=['Speed_mph'])

# Establece el título y las etiquetas de los ejes
fig.update_layout(title='Coaster Speed (mph)', xaxis_title='Speed (mph)')

# Muestra el gráfico
fig.show()


# In[149]:


# Crea un gráfico de densidad para la columna 'Speed_mph'
fig = go.Figure()
fig.add_trace(go.Histogram(x=df_procesed['Speed_mph'], histnorm='probability density'))

# Establece el título y las etiquetas de los ejes
fig.update_layout(title='Coaster Speed (mph)', xaxis_title='Speed (mph)')

# Muestra el gráfico
fig.show()


# In[150]:


ax = df_procesed['Speed_mph'].plot(kind='kde',
                          title='Coaster Speed (mph)')
ax.set_xlabel('Speed (mph)')


# In[151]:


ax = df_procesed['Year_Introduced'].value_counts() \
    .head(10) \
    .plot(kind='bar', title='Top 10 Years Coasters Introduced')
ax.set_xlabel('Year Introduced')
ax.set_ylabel('Count')


# In[152]:


num_var = df_procesed.select_dtypes(include=[np.number]).columns
num_var


# In[153]:


# Crea una lista vacía para almacenar los gráficos de caja
box_plots = []

# Crea un gráfico de caja para cada columna numérica
for col in num_var:
    box_plots.append(go.Box(y=df_clean[col], name=col))

# Muestra los gráficos de caja en una cuadrícula
fig = plotly.subplots.make_subplots(rows=2, cols=4, subplot_titles=num_var)
for i, plot in enumerate(box_plots):
    row = i // 4 + 1
    col = i % 4 + 1
    fig.add_trace(plot, row=row, col=col)

fig.show()


# In[154]:


fig, axes = plt.subplots(nrows=2, ncols=4, figsize=(12, 6))
for i, col in enumerate(num_var):
    row = i // 4
    col_idx = i % 4
    df.boxplot(column=col, ax=axes[row, col_idx])

# Muestra el resultado
plt.show()


# In[155]:


df_procesed.columns


# In[156]:


import plotly.figure_factory as ff
import plotly.subplots

# Crea una lista vacía para almacenar los gráficos de violín
violin_plots = []

# Crea un gráfico de violín para cada columna numérica
for col in num_var:
    violin_plots.append(ff.create_violin(df_clean, data_header=col, group_header='Type_Main', title=col))

# Muestra los gráficos de violín en una cuadrícula
fig = plotly.subplots.make_subplots(rows=2, cols=4, subplot_titles=num_var)
for i, plot in enumerate(violin_plots):
    row = i // 4 + 1
    col = i % 4 + 1
    for trace in plot.data:
        fig.add_trace(trace, row=row, col=col)

# Ajusta el tamaño de la figura a (800, 600)
fig.update_layout(width=800, height=600)

fig.show()


# In[157]:


fig, axes = plt.subplots(nrows=2, ncols=4, figsize=(12, 6))

for i, col in enumerate(num_var):
    row = i // 4
    col_idx = i % 4
    sns.violinplot(x='Type_Main', y=col, data=df_procesed, ax=axes[row, col_idx])

# Muestra el resultado
plt.show()


# In[163]:


df_clean.head()


# In[159]:


ax = df_procesed.query('Location != "Other"').groupby('Location')['Speed_mph'].agg(['mean','count']).query('count >= 10').sort_values('mean')['mean'].plot(kind='barh', figsize=(12, 5), title='Average Coast Speed by Location')
ax.set_xlabel('Average Coaster Speed')
plt.show()


# In[160]:


# Elimina las filas con valores NaN
df_clean = df.dropna()

# Selecciona los valores únicos de la columna 'Type_Main'
unique_values = df_clean['Coaster_Name'].unique()

filtered_df = df_clean[df_clean['Coaster_Name'].isin(unique_values)]

# Selecciona solo las columnas 'Coaster_Name', 'Longitud' y 'Latitud'
df_folium = filtered_df[['Coaster_Name', 'latitude', 'longitude']]


# In[161]:


df_folium.isna().sum()


# In[162]:


m = folium.Map(location=[df_folium['latitude'].iloc[0], df_folium['longitude'].iloc[0]],zoom_start=2)

# Agrega un marcador al mapa para cada montaña rusa en la lista de valores únicos
for index, row in df_folium.iterrows():
    icon = folium.Icon(color='red', icon_size=(20, 20))
    folium.Marker(location=[row['latitude'], row['longitude']], icon=icon).add_to(m)

m


# In[ ]:





# In[ ]:




