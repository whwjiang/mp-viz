import React from 'react'
import PropTypes from 'prop-types'

import './App.css';

const RouteView = ({ route }) => {
    const nullCheck = (route === null);
    return (
    <>
        {nullCheck ? ( <>
            <div className='center'> 
                <p>none!</p>
            </div>
        </> ) : ( <>
            <div className='center'>
                <img 
                    src={route.image_urls[0]}
                    alt="route"
                    className="routePicture"
                />
            </div>
            <br></br>
            <div className="center">
                <a 
                    className='center black-text' 
                    href={route.url}>
                        <b>{route.name}</b>
                    </a>
            </div>
            <div className="center">
                <li>Grade: {route.grade}</li>
                <li>Rating: {route.rating}/4 on {route.rating_count} votes</li>
            </div>
        </> )}
    </>
    );
}

RouteView.propTypes = {
    route: PropTypes.object.isRequired
}

export default RouteView;