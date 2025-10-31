//components//ItemCard.js
import React, { useState } from 'react';
import axios from 'axios';

function ItemCard({ item, email }) {
  const [showPopup, setShowPopup] = useState(false);

  const handleClaim = async (status) => {
    try {
      await axios.post('http://127.0.0.1:5000/confirm-item', {
        filename: item.filename,
        email,
        status
      });
      alert(status === 'claimed' ? "Thank you! Item claimed." : "Noted!");
      setShowPopup(false);
    } catch (err) {
      console.error(err);
      alert("Error sending claim");
    }
  };

  return (
    <div className="item-card" onClick={() => setShowPopup(true)}>
      <img src={`http://127.0.0.1:5000/${item.image_path}`} alt={item.filename} />
      <div>
        <h3>{item.filename}</h3>
        <p>{item.description}</p>
      </div>

      {showPopup && (
        <div className="popup">
          <p>Is this your item?</p>
          <button onClick={() => handleClaim('claimed')}>Yes</button>
          <button onClick={() => handleClaim('pending')}>No</button>
        </div>
      )}
    </div>
  );
}

export default ItemCard;
