import React, { useEffect, useState } from 'react';
import './styles.css';
import img1 from './images/binarydot.jpg';
import img2 from './images/whitepaper.jpg';
import img3 from './images/aboutus.jpg';
import img4 from './images/blog.jpg';
import axios from 'axios';

function Home() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    axios.get('http://localhost:3001/users') // Correct endpoint for fetching users
      .then(response => {
        if (response.data.length > 0) {
          setUser(response.data[0]); // Assuming you want the first user
        }
      })
      .catch(err => console.log(err));
  }, []);

  return (
    <div>
      <div className="linkedin">Welcome {user ? user.name : 'Guest'}!</div>
      <div className="main">
        <img src={img1} alt="Binary Dot" />
      </div>
      <div className="sub-container">
        <div className="sub1">
          <img src={img1} alt="Binary Dot" />
        </div>
        <div className="sub2">
          <img src={img2} alt="White Paper" />
        </div>
      </div>
      <div className='sub-container1'>
        <div className='sub3'>
          <img src={img3} alt="About Us" />
        </div>
        <div className='sub4'>
          <img src={img4} alt="Blog" />
        </div>
      </div>
    </div>
  );
}

export default Home;
