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
  const [successMessage, setSuccessMessage] = useState("");
  const [showHome, setShowHome] = useState(true);

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

      // Handle "Item Not Found"
      if (!data || data.length === 0 || data.message === "Item Not Found.") {
        setNotFound(true);
        return;
      }

      // Matches found → show popup
      setMatchedItems(data);
      setSelectedItem(data[0]);
      setShowPopup(true);

    } catch (error) {
      console.error("Error fetching items:", error);
    }
  };

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
        setSuccessMessage(
          `This is your item ✅ Please contact Help Desk Center in Sahyadri College, Mangaluru.`
        );
        setThankYou(true);
      } catch (error) {
        console.error("Error confirming item:", error);
      }
    } else if (!isOwner) {
      setNoResponseMessage(true);
    }
  };

  // ----- Render Homepage -----
  if (showHome) {
    return (
      <div className="homepage">
        <div className="homepage-overlay">
          <h1>Lost Item Matcher</h1>
          <p>
            Welcome to Lost Item Matcher! Quickly find lost items or report them.
          </p>
          <button className="btn" onClick={() => setShowHome(false)}>
            Get Started
          </button>
        </div>
      </div>
    );
  }

  // ----- Render Main Form and Other UI -----
  return (
    <div className="container">
      <h1 className="title">Lost Item Matcher</h1>

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
          placeholder="Email (optional)"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <button type="submit" className="btn">
          Find Item
        </button>
      </form>

      {/* Matched Items (if not showing popup) */}
      {matchedItems.length > 0 && !showPopup && (
        <div className="items-container">
          {matchedItems.map((item, index) => (
            <div className="item-card" key={index}>
              <img
                src={`http://127.0.0.1:5000/${item.image_path}`}
                alt={item.filename}
              />
              <h3>{item.filename}</h3>
              <p>{item.description}</p>
            </div>
          ))}
        </div>
      )}

      {/* Popup for Yes/No */}
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
            <h2>🎉 Item Confirmed!</h2>
            {selectedItem && (
              <img
                src={`http://127.0.0.1:5000/${selectedItem.image_path}`}
                alt={selectedItem.filename}
                className="popup-image"
                style={{ maxWidth: "200px", margin: "1rem 0" }}
              />
            )}
            <p>{successMessage}</p>
            <button onClick={() => setThankYou(false)} className="popup-close-btn">
              Close
            </button>
          </div>
        </div>
      )}

      {/* Item Not Found Popup */}
      {notFound && (
        <div className="overlay">
          <div className="popup-card notfound-card">
            <h2>❌ Item Not Found</h2>
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
                  setSuccessMessage(
                    "Thank you! You will be notified if a matching item is added."
                  );
                  setThankYou(true);
                  setNotFound(false);
                } catch (error) {
                  console.error("Error adding notification:", error);
                }
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
