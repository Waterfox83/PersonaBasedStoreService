# Persona Driven Stores: APIs

Wireframes: [https://marvelapp.com/ajjg47h/screen/53196383](https://marvelapp.com/ajjg47h/screen/53196383)

- Get all personas given **gender**

- --Each persona should have
  - --Persona Name,
  - --Persona Image
  - --Category and {attribute, value} pairs for each attribute of the category.
  - --Location of substore

- Get all categories and corresponding attributes and values given **gender**
- Get cluster/persona information given the dictionary of {attribute, attribute value}
  - Result should have, array of personas.

#### APIs

| Method | Request | Description |
| --- | --- | --- |
| GET | **api/v1/categories/{gender}** | Get all categories given gender |
| GET | **api/v1/personas/{gender}** | Get all personas given gender |
| POST | **api/v1/personas/computed** | Get computed cluster/persona information given the dictionary of {attribute, attribute value} and gender information  |

#### Request/Response

##### GET: /api/v1/categories/{gender}

###### Request

````
GET _/api/v1/categories/{gender}
````

###### Response [HTTP Status: 200]

````
[{
        "Dresses": [{
            "Silhouette": ["Sheath", "Shift", "Trapeze"],
            "Sleeve Length": ["Sleeveless", "Long", "Short", "3/4 Sleeve"],
            "Material": ["Woven", "Knit", "Sweater"]
        }]
    },
    {
        "Denim": [{
            "Rise": ["Mid", "High", "Low"],
            "Color": ["Black", "Dark", "Medium"]
        }]
    }
]
````

##### GET: /api/v1/personas/{gender}

###### Request

````
GET _/api/v1/personas/{gender}
````

###### Response [HTTP Status: 200]

````
[
 {
   "Name": "Persona 1",
   "Location": "L1",
   "Properties": [
     {
       "Dress": [
         {
           "Silhouette": [
             "Sheath"
           ],
           "Sleeve Length": [
             "Sleeveless","Short"
           ],
           "Material": [
             "Woven"
           ]
         }
       ]
     },
     {
       "Denim": [
         {
           "Rise": [
             "Mid"
           ],
           "Color": [
             "Black"
           ]
         }
       ]
     }
   ]
 },
 {
   "Name": "Persona 2",
   "Location": "L2",
   "Properties": [
     {
       "Dress": [
         {
           "Silhouette": [
             "Shift"
           ],
           "Sleeve Length": [
             "Long"
           ],
           "Material": [
             "Knit"
           ]
         }
       ]
     },
     {
       "Denim": [
         {
           "Rise": [
             "High"
           ],
           "Color": [
             "Medium"
           ]
         }
       ]
     }
   ]
 }
]
````

##### POST: /api/v1/personas/computed

###### Request

````
POST: /api/v1/personas

{
“Gender” :”male”,
“selectedAttributes”:
[
 {
   "Dress": [
     {
       "Silhouette": [
         "Sheath"
       ],
       "Sleeve Length": [
         "Sleeveless", "Short"
       ],
       "Material": [
         "Woven"
       ]
     }
   ]
 },
 {
   "Denim": [
     {
       "Rise": [
         "Mid"
       ],
       "Color": [
         "Black"
       ]
     }
   ]
 }
]
}
 
````

###### Response [HTTP Status: 200]

````
[
 {
   "Name": "Persona 1",
   "Location": "L1",
   "Properties": [
     {
       "Dress": [
         {
           "Silhouette": [
             "Sheath"
           ],
           "Sleeve Length": [
             "Sleeveless","Short"
           ],
           "Material": [
             "Woven"
           ]
         }
       ]
     },
     {
       "Denim": [
         {
           "Rise": [
             "Mid"
           ],
           "Color": [
             "Black"
           ]
         }
       ]
     }
   ]
 },
 {
   "Name": "Persona 2",
   "Location": "L2",
   "Properties": [
     {
       "Dress": [
         {
           "Silhouette": [
             "Shift"
           ],
           "Sleeve Length": [
             "Long"
           ],
           "Material": [
             "Knit"
           ]
         }
       ]
     },
     {
       "Denim": [
         {
           "Rise": [
             "High"
           ],
           "Color": [
             "Medium"
           ]
         }
       ]
     }
   ]
 }
]
````