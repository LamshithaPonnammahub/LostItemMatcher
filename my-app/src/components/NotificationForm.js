import React, { useState } from 'react';
import axios from 'axios';

function NotificationForm({ description, email }) {
  const [userEmail, setUserEmail] = useState(email || '');

  const handleSubmit = async () => {
    try {
      await axios.post('http://127.0.0.1:5000/add-notification', {
        description,
        email: userEmail
      });
      alert("You will be notified if a matching item is added!");
    } catch (err) {
      console.error(err);
      alert("Error adding notification");
    }
  };

  return (
    <div className="popup">
      <p>Sorry! No match found.</p>
      <input placeholder="Enter your email" value={userEmail} onChange={e => setUserEmail(e.target.value)} />
      <button onClick={handleSubmit}>Submit</button>
    </div>
  );
}

export default NotificationForm;
