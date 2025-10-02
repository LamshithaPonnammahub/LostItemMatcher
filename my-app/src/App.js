import React, { useState } from "react";
import "./styles.css";

function App() {
  const [type, setType] = useState("");
  const [color, setColor] = useState("");
  const [description, setDescription] = useState("");
  const [email, setEmail] = useState("");
  const [matchedItems, setMatchedItems] = useState([]);
  const [showPopup, setShowPopup] = useState(false);
  const [selectedItem, setSelectedItem] = useState(null);
  const [notFound, setNotFound] = useState(false);
  const [thankYou, setThankYou] = useState(false);
  const [noResponseMessage, setNoResponseMessage] = useState(false);

  // Submit user input
  const handleSubmit = async (e) => {
    e.preventDefault();
    setMatchedItems([]);
    setShowPopup(false);
    setNotFound(false);
    setThankYou(false);
    setNoResponseMessage(false);

    const userItem = { type, color, description, email };

    try {
      const response = await fetch("http://127.0.0.1:5000/find-item", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(userItem),
      });

      const data = await response.json();

      if (data.length === 0) {
        setNotFound(true);
      } else {
        // Find the most exact match
        const match = data.find(
          (item) =>
            item.type.toLowerCase() === type.toLowerCase() &&
            item.color.toLowerCase() === color.toLowerCase() &&
            item.description.toLowerCase() === description.toLowerCase()
        ) || data[0];

        setMatchedItems(data);
        setSelectedItem(match);
        setShowPopup(true);
      }
    } catch (error) {
      console.error("Error fetching items:", error);
    }
  };

  // Handle Yes/No on popup
  const handlePopupResponse = async (isOwner) => {
    setShowPopup(false);
    if (isOwner && selectedItem) {
      try {
        await fetch("http://127.0.0.1:5000/confirm-item", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            filename: selectedItem.filename,
            email,
            description: selectedItem.description,
            status: "claimed",
          }),
        });
      } catch (error) {
        console.error("Error confirming item:", error);
      }
      setThankYou(true);
    } else if (!isOwner) {
      setNoResponseMessage(true);
    }
  };

  return (
    <div className="container">
      <h1 className="title">Lost Item Matcher</h1>

      {/* Input Form */}
      <form className="form" onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Type (bottle, umbrella...)"
          value={type}
          onChange={(e) => setType(e.target.value)}
          required
        />
        <input
          type="text"
          placeholder="Color"
          value={color}
          onChange={(e) => setColor(e.target.value)}
          required
        />
        <input
          type="text"
          placeholder="Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          required
        />
        <input
          type="email"
          placeholder="Your Email (optional)"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <button type="submit" className="btn">
          Find Item
        </button>
      </form>

      {/* Matched Items */}
      {matchedItems.length > 0 && !showPopup && (
        <div className="items-container">
          {matchedItems.map((item, index) => (
            <div className="item-card" key={index}>
              <img
                src={`http://127.0.0.1:5000/${item.image_path}`}
                alt={item.filename}
              />
              <div>
                <h3>{item.filename}</h3>
                <p>{item.description}</p>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Popup for Confirming Item */}
      {showPopup && selectedItem && (
        <div className="overlay">
          <div className="popup-card">
            <h2>Is this your item?</h2>
            <img
              src={`http://127.0.0.1:5000/${selectedItem.image_path}`}
              alt={selectedItem.filename}
              className="popup-image"
            />
            <p>{selectedItem.description}</p>
            <div className="popup-buttons">
              <button onClick={() => handlePopupResponse(true)}>Yes</button>
              <button onClick={() => handlePopupResponse(false)}>No</button>
            </div>
          </div>
        </div>
      )}

      {/* Thank You Popup */}
      {thankYou && (
        <div className="overlay">
          <div className="popup-card thank-you-card">
            <h2>🎉 Thank you!</h2>
            <p>Your item is successfully marked as claimed.</p>
            <img
              src="https://media.giphy.com/media/111ebonMs90YLu/giphy.gif"
              alt="celebration"
              className="thank-you-image"
            />
            <button
              onClick={() => setThankYou(false)}
              className="popup-close-btn"
            >
              Close
            </button>
          </div>
        </div>
      )}

      {/* Item Not Found */}
      {notFound && (
        <div className="overlay">
          <div className="popup-card notfound-card">
            <h2>❌ Sorry! No item found.</h2>
            <p>Enter your email to get notified if a similar item is added:</p>
            <input
              type="email"
              placeholder="Your Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            <button
              onClick={async () => {
                try {
                  await fetch("http://127.0.0.1:5000/add-notification", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ description, email }),
                  });
                } catch (error) {
                  console.error("Error adding notification:", error);
                }
                setThankYou(true);
                setNotFound(false);
              }}
            >
              Submit
            </button>
          </div>
        </div>
      )}

      {/* No Response Message */}
      {noResponseMessage && (
        <div className="overlay">
          <div className="popup-card noresponse-card">
            <h2>ℹ️ Your email will be saved!</h2>
            <p>
              If new items matching your description are added in the future, we
              will contact you.
            </p>
            <button
              onClick={() => setNoResponseMessage(false)}
              className="popup-close-btn"
            >
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
