import React, { useState, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faMugSaucer, faBowlFood, faUtensils, faUser, faCookieBite } from '@fortawesome/free-solid-svg-icons'
import './styles/App.css';

function App() {

  // const express = require('express');
  // const cors = require('cors');
  // const app = express();
  // app.use(cors());

  /* fetch data */

  const [biteData, setBiteData] = useState({});
  const [isLoading, setIsLoading] = useState(true);

  const apiUrl = 'https://a4d2-192-54-222-148.ngrok-free.app/data';

  let displayData;
  let feedback;
  useEffect(() => {
    // Make a GET request to the server's API
    fetch(apiUrl, {
      method: 'GET',
      mode: 'cors'
    })
      .then(response => response.json())
      .then(data => {
        setBiteData(data);
        setIsLoading(false);
      })
      .catch((error) => {
        console.error('Error fetching Bite data :', error);
        setIsLoading(false);
      });
  }, []);


  return (
    <div className="App">
      <div className="navbar">
        <ul className="nav-list">
          <div className="nav-title-container">
            <div className="logo-container"><FontAwesomeIcon icon={faCookieBite} className="bite-logo" /></div>
            <div className="nav-title">Bite</div>
          </div>
          <div className="nav-1">
            <div className="calorie-container">
              <div className="calorie-stat">2,100</div>
              <div className="calorie-type">Calories</div>
            </div>
          </div>
          <div className="nav-2">
            <div className="nav-stat macro-container">
              <div className="macro-stat">8 cups</div>
              <div className="macro-type">Water</div>
            </div>
            <div className="nav-stat macro-container">
              <div className="macro-stat">30g</div>
              <div className="macro-type">Protein</div>
            </div>
            <div className="nav-stat macro-container">
              <div className="macro-stat">250g</div>
              <div className="macro-type">Carbs</div>
            </div>
            <div className="nav-stat macro-container">
              <div className="macro-stat">32g</div>
              <div className="macro-type">Fats</div>
            </div>
          </div>
          <div className="nav-3">
            <div className="nav-stat micro-container">
              <div className="micro-stat">300mg</div>
              <div className="micro-type">Vitamins</div>
            </div>
            <div className="nav-stat micro-container">
              <div className="micro-stat">1kg</div>
              <div className="micro-type">Minerals</div>
            </div>
          </div>
          <div className="nav-profile">
            <button><FontAwesomeIcon icon={faUser} className="user-icon" /></button>
          </div>
        </ul>
      </div>
      <main>
        <div className="card dashboard-container">
          <div className="dashboard">
            <div className="dashboard-top">
              <h1>Your Meals</h1>
              All your nutrition. In one place.
            </div>
            <div className="dashboard-catalog">
              <span className="date">Date</span>
              <span className="time">#</span>
              <span className="name">Meal</span>
              <span className="calorie-count">Calories</span>
              <span className="meal">Type of Meal</span>
            </div>
            <ul className="food-list">
              <li>
                <span className="date">Today</span>
                <span className="time">1</span>
                <span className="name">Willage</span>
                <span className="calorie-count">553kcal</span>
                <span className="meal"><FontAwesomeIcon icon={faUtensils} /></span>
              </li>
              <li>
                <span className="date">Today</span>
                <span className="time">2</span>
                <span className="name">Panda Express</span>
                <span className="calorie-count">950kcal</span>
                <span className="meal"><FontAwesomeIcon icon={faBowlFood} /></span>
              </li>
              <li>
                <span className="date">Today</span>
                <span className="time">3</span>
                <span className="name">Ramen</span>
                <span className="calorie-count">730kcal</span>
                <span className="meal"><FontAwesomeIcon icon={faMugSaucer} /></span>
              </li>
              {
                biteData && biteData.meals ? (
                    biteData.meals.map((meal, index) => (
                    <li key={index}>
                      <span className="date">Today</span>
                      <span className="time">{index + 4}</span>
                      <span className="meal">{meal["Food Name"]}</span>
                      <span className="calorie-count">{meal["Nutritional Info"]["Calories"]["quantity"] + meal["Nutritional Info"]["Calories"]["unit"]}</span>
                      <span className="meal"><FontAwesomeIcon icon={faUtensils} /></span>
                    </li>
                  ))
                ) : (
                  <p>Loading...</p>
                )
              }
            </ul>
            {/* List of everything you've eaten */
            /* Display calories, macronutrients, nutrients, vitamin, protein, carbs, etc. for each food */}
            <div className="summary-box">
              {/* Display the sum of all calories, proteins, carbs, macronutrients & vitamin */
              /* Color code based on data quality */}
            </div>
          </div>
        </div>
        <div className="nutrition">
          <section className="performance-facts">
            <header className="performance-facts__header">
              <h1 className="performance-facts__title">Nutrition Facts</h1>
              <div>Serving Size 1/2 cup (about 82g)
                <p>Serving Per Container 8</p>
              </div>
            </header>
            <table className="performance-facts__table">
              <thead>
                <tr>
                  <th colSpan="3" className="small-info">
                    Amount Per Serving
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <th colSpan="2">
                    <b>Calories</b>
                    200
                  </th>
                  <td>
                    Calories from Fat
                    130
                  </td>
                </tr>
                <tr className="thick-row">
                  <td colSpan="3" className="small-info">
                    <b>% Daily Value*</b>
                  </td>
                </tr>
                <tr>
                  <th colSpan="2">
                    <b>Total Fat</b>
                    14g
                  </th>
                  <td>
                    <b>22%</b>
                  </td>
                </tr>
                <tr>
                  <td className="blank-cell">
                  </td>
                  <th>
                    Saturated Fat
                    9g
                  </th>
                  <td>
                    <b>22%</b>
                  </td>
                </tr>
                <tr>
                  <td className="blank-cell">
                  </td>
                  <th>
                    Trans Fat
                    0g
                  </th>
                  <td>
                  </td>
                </tr>
                <tr>
                  <th colSpan="2">
                    <b>Cholesterol</b>
                    55mg
                  </th>
                  <td>
                    <b>18%</b>
                  </td>
                </tr>
                <tr>
                  <th colSpan="2">
                    <b>Sodium</b>
                    40mg
                  </th>
                  <td>
                    <b>2%</b>
                  </td>
                </tr>
                <tr>
                  <th colSpan="2">
                    <b>Total Carbohydrate</b>
                    17g
                  </th>
                  <td>
                    <b>6%</b>
                  </td>
                </tr>
                <tr>
                  <td className="blank-cell">
                  </td>
                  <th>
                    Dietary Fiber
                    1g
                  </th>
                  <td>
                    <b>4%</b>
                  </td>
                </tr>
                <tr>
                  <td className="blank-cell">
                  </td>
                  <th>
                    Sugars
                    14g
                  </th>
                  <td>
                  </td>
                </tr>
                <tr className="thick-end">
                  <th colSpan="2">
                    <b>Protein</b>
                    3g
                  </th>
                  <td>
                  </td>
                </tr>
              </tbody>
            </table>

            <table className="performance-facts__table--grid">
              <tbody>
                <tr>
                  <td colSpan="2">
                    Vitamin A
                    10%
                  </td>
                  <td>
                    Vitamin C
                    0%
                  </td>
                </tr>
                <tr className="thin-end">
                  <td colSpan="2">
                    Calcium
                    10%
                  </td>
                  <td>
                    Iron
                    6%
                  </td>
                </tr>
              </tbody>
            </table>

            <p className="small-info">* Percent Daily Values are based on a 2,000 calorie diet. Your daily values may be higher or lower depending on your calorie needs:</p>

            <table className="performance-facts__table--small small-info">
              <thead>
                <tr>
                  <td colSpan="2"></td>
                  <th>Calories:</th>
                  <th>2,000</th>
                  <th>2,500</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <th colSpan="2">Total Fat</th>
                  <td>Less than</td>
                  <td>65g</td>
                  <td>80g</td>
                </tr>
                <tr>
                  <td className="blank-cell"></td>
                  <th>Saturated Fat</th>
                  <td>Less than</td>
                  <td>20g</td>
                  <td>25g</td>
                </tr>
                <tr>
                  <th colSpan="2">Cholesterol</th>
                  <td>Less than</td>
                  <td>300mg</td>
                  <td>300 mg</td>
                </tr>
                <tr>
                  <th colSpan="2">Sodium</th>
                  <td>Less than</td>
                  <td>2,400mg</td>
                  <td>2,400mg</td>
                </tr>
                <tr>
                  <th colSpan="3">Total Carbohydrate</th>
                  <td>300g</td>
                  <td>375g</td>
                </tr>
                <tr>
                  <td className="blank-cell"></td>
                  <th colSpan="2">Dietary Fiber</th>
                  <td>25g</td>
                  <td>30g</td>
                </tr>
              </tbody>
            </table>

            <p className="small-info">
              Calories per gram:
            </p>
            <p className="small-info text-center">
              Fat 9
              &bull;
              Carbohydrate 4
              &bull;
              Protein 4
            </p>

          </section>
        </div>
        

        <div className="card chatbot">
          <h1>Feedback</h1>
          Today's personal nutrition feedback.
          {
            isLoading ? (
              <p className="chatbot-text">Loading...</p>
            ) : (
              <p className="chatbot-text">{biteData.agg?.chatgpt}</p>
            )
          }
          {/* Provide dietary advice for the next few days */
          /* Interact with user's data */}
        </div>
      </main>
    </div>
  );
}

export default App;