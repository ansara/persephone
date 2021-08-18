import React, {Component} from 'react';
import { Form, Button, Col, Container } from 'react-bootstrap';

class InputDetails extends Component {
    render() {
        return(
        <Container>
                <Form>
                    <Form.Row>
                        <Form.Group as={Col} controlId="formFirstName">
                            <Form.Label className="label">First Name</Form.Label>
                            <Form.Control
                            type="text"
                            placeholder='Jane'
                            name="firstName"
                            required
                            onChange={this.props.handleChange}
                            />
                        </Form.Group>

                        <Form.Group as={Col} controlId="formLastName">
                            <Form.Label className="label">Initial of Last Name (optional)</Form.Label> 
                            <Form.Control
                            type="text"
                            placeholder='D'
                            name="lastName"
                            onChange={this.props.handleChange}
                            />
                        </Form.Group>
                    </Form.Row>
                    <Form.Row>
                        <Form.Group as={Col} controlId="formLocation">
                            <Form.Label>Location</Form.Label>
                            <Form.Control as="select" name="location" required onChange={this.props.handleChange}>
                                <option default=""></option>
                                <optgroup label="US States:">
                                <option value="AL">Alabama</option>
                                <option value="AK">Alaska</option>
                                <option value="AZ">Arizona</option>
                                <option value="AR">Arkansas</option>
                                <option value="CA">California</option>
                                <option value="CO">Colorado</option>
                                <option value="CT">Connecticut</option>
                                <option value="DE">Delaware</option>
                                <option value="DC">District Of Columbia</option>
                                <option value="FL">Florida</option>
                                <option value="GA">Georgia</option>
                                <option value="HI">Hawaii</option>
                                <option value="ID">Idaho</option>
                                <option value="IL">Illinois</option>
                                <option value="IN">Indiana</option>
                                <option value="IA">Iowa</option>
                                <option value="KS">Kansas</option>
                                <option value="KY">Kentucky</option>
                                <option value="LA">Louisiana</option>
                                <option value="ME">Maine</option>
                                <option value="MD">Maryland</option>
                                <option value="MA">Massachusetts</option>
                                <option value="MI">Michigan</option>
                                <option value="MN">Minnesota</option>
                                <option value="MS">Mississippi</option>
                                <option value="MO">Missouri</option>
                                <option value="MT">Montana</option>
                                <option value="NE">Nebraska</option>
                                <option value="NV">Nevada</option>
                                <option value="NH">New Hampshire</option>
                                <option value="NJ">New Jersey</option>
                                <option value="NM">New Mexico</option>
                                <option value="NY">New York</option>
                                <option value="NC">North Carolina</option>
                                <option value="ND">North Dakota</option>
                                <option value="OH">Ohio</option>
                                <option value="OK">Oklahoma</option>
                                <option value="OR">Oregon</option>
                                <option value="PA">Pennsylvania</option>
                                <option value="RI">Rhode Island</option>
                                <option value="SC">South Carolina</option>
                                <option value="SD">South Dakota</option>
                                <option value="TN">Tennessee</option>
                                <option value="TX">Texas</option>
                                <option value="UT">Utah</option>
                                <option value="VT">Vermont</option>
                                <option value="VA">Virginia</option>
                                <option value="WA">Washington</option>
                                <option value="WV">West Virginia</option>
                                <option value="WI">Wisconsin</option>
                                <option value="WY">Wyoming</option>
                                </optgroup>
                                <optgroup label="Countries:">
                                <option value="CAN">Canada</option>
                                <option value="DEN">Denmark</option>
                                <option value="GER">Germany</option>
                                <option value="IT">Italy</option>
                                <option value="NL">Netherlands</option>
                                <option value="SWE">Sweden</option>
                                <option value="UK">United Kingdom</option>
                                </optgroup>
                            </Form.Control>
                        </Form.Group>
                    </Form.Row>
                    <Form.Row>                        
                    <Button variant="primary" onClick={this.submit}>Search</Button>
                    </Form.Row>
                </Form>
            </Container>
            );
    }
}
export default InputDetails;