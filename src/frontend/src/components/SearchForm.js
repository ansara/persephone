import React, {Component} from 'react';
import InputDetails from './InputDetails'
import MatchFound from './MatchFound'
import NotFound from './NotFound'

class SearchForm extends Component{

    state = {
        step: 1,
        firstName: '',
        lastInitial: '',
        location: '',
    }

    nextStep = () => {
        const { step } = this.state
        this.setState({
            step : step + 1
        })
    }

    prevStep = () => {
        const { step } = this.state
        this.setState({
            step : step - 1
        })
    }

    handleChange = (event) => {
        this.setState({[event.target.name]: event.target.value})
    }

    render() {
        const { step, firstName, lastInitial, location } = this.state;
        const inputValues = { firstName, lastInitial, location };
        switch(step){
            case 1:
                return <InputDetails
                nextStep = {this.nextStep}
                handleChange={this.handleChange}
                inputValues={inputValues}
                />
            case 2:
                return <MatchFound
                nextStep = {this.nextStep}
                prevStep = {this.prevStep}
                handleChange={this.handleChange}
                inputValues={inputValues}/>
            case 3:
                return <NotFound
                nextStep={this.nextStep}
                prevStep={this.prevStep}
                handleChange={this.handleChange}
                inputValues={inputValues}
                />
        }
    }
}

export default SearchForm;