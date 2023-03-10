// TODO ESLINT OVERRIDES
/* eslint-disable jsx-a11y/anchor-is-valid */

// TODO https://reactjs.org/docs/faq-ajax.html#example-using-ajax-results-to-set-local-state
import { useState,  useEffect } from 'react';
import {
  useParams,
  useNavigate,
  useLocation,
  Outlet,
  useSearchParams
} from "react-router-dom";
import { config } from '../../Constants'
import IPRS_Person from './resource'
import { updateQueryStringParameter, getQueryVariable } from '../../utility/url';
import { handleErrorAxios } from '../../utility/notification';
import { getParameterByName } from '../../utility/url';
import { getResources } from '../../services/countries';

const axios = require('axios').default;

// TODO https://a-carreras-c.medium.com/development-and-production-variables-for-react-apps-c04af8b430a5
var url = config.url.API_URL
// var url_users = config.url.API_URL_USERS

export default function Collection() {
  const [isLoaded, setIsLoaded] = useState(false);
  const [resources, setResources] = useState([]);
  const [pagination, setPagination] = useState([]);

  let navigate = useNavigate();
  let location = useLocation();
  let params = useParams();
  let [searchParams, setSearchParams] = useSearchParams();

  let police_station = null;

  // TODO https://axios-http.com/docs/instance
  // const instance = axios.create({
  //   baseURL: url,
  //   timeout: 1000,
  //   // headers: {'X-Custom-Header': 'foobar'},
  //   // TODO https://axios-http.com/docs/handling_errors
  //   // validateStatus: function (status) {
  //   //   return status < 500; // Resolve only if the status code is less than 500
  //   // }
  // });

  // Note: the empty deps array [] means
  // this useEffect will run once
  // similar to componentDidMount()
  useEffect(() => {
    const police_station = getQueryVariable("police_station");
    if(police_station) {
      window.police_station = police_station;
      // getResources({police_station: station});
    }
    // else {
    //   getResources({police_station: window.police_station});
    // }
    getResources();
  }, [params, location.search])

  // if (error) {
  //   return <div>Error: {error.message}</div>;
  // } else if (!isLoaded) {
  //   return <div>Loading...</div>;
  // } else {
  //   return (
  //     <ul>
  //       {items.map(item => (
  //         <li key={item.id}>
  //           {item.name} {item.price}
  //         </li>
  //       ))}
  //     </ul>
  //   );

  function getResources(params={}) {
    const page = getParameterByName('page');

    // axios.get(`${url}/vps/api/v0/occurrences`, {params})
    axios.get(`${url}/vps/api/v0/occurrences`, {
      params: {
        // ID: 12345
        police_station: window.police_station,
        page: page ? page : 1
      }
    })
    .then(function (response) {
      // handle success
      console.log(response);
      setIsLoaded(true);
      setResources(response.data.results);

      const pagination = {
        'previous': response.data.previous,
        'next': response.data.next
      }
      setPagination(pagination);
    })
    .catch(function(error){
      // handle error
      console.error(error);
      setIsLoaded(true);
      
      handleErrorAxios(error)
    })
    .then(function () {
      // always executed
    });
  }

  function getResource(id, module, e) {
    switch (module) {
      case 'OB':
        navigate('/vps/occurrence-book/'+id);
        break;
    
      default:
        break;
    }
  }

  function navigatePagination(page, e) {
    if (page) {
      setSearchParams({police_station: window.police_station, page: page});
    }
  }

  // This is a react js component
  function Reporters(props) {
    let reporters = [];
    for(const index in props.reporters) {
      const full_name = props.reporters[index].iprs_person.first_name + " " + props.reporters[index].iprs_person.last_name
      const id_no = props.reporters[index].iprs_person.id_no
      ? `_${props.reporters[index].iprs_person.id_no} `
      : props.reporters[index].iprs_person.passport_no ? `_ ${props.reporters[index].iprs_person.passport_no} ` : ' '

      reporters.push(full_name + id_no)
    }

    return reporters 
  }

  return (
    <div className="row" style={{ display: 'block' }}>
      <div className="col-md-12 col-sm-12  ">
        <div className="x_panel">
            <div className="x_title">
            <h2>
              {/* Police Officer <small>Police Officers in the world</small> */}
            </h2>
            <ul className="nav navbar-right panel_toolbox">
                <li>
                  <a
                    className="">
                      (page: {getParameterByName('page') ? getParameterByName('page'): 1})
                    </a>
                </li>
                <li>
                  <a
                    className=""
                    onClick={(e) => navigatePagination(getParameterByName('page', pagination.previous) ? getParameterByName('page', pagination.previous) : 1)}>
                      <i className="fa fa-chevron-left"></i>
                    </a>
                </li>
                <li>
                  <a
                    className=""
                    onClick={(e) => navigatePagination(1)}>
                      1
                    </a>
                </li>
                {/* <li><a className=""><i className="fa fa-chevron-up"></i></a>
                </li> */}
                <li>
                  <a
                    className=""
                    onClick={(e) => navigatePagination(getParameterByName('page', pagination.next))}>
                      <i className="fa fa-chevron-right"></i>
                  </a>
                </li>
                {/* <li><a className="collapse-link"><i className="fa fa-chevron-up"></i></a>
                </li>
                <li className="dropdown">
                <a href="#" className="dropdown-toggle" data-toggle="dropdown" role="button" aria-expanded="false"><i className="fa fa-wrench"></i></a>
                <div className="dropdown-menu" aria-labelledby="dropdownMenuButton">
                    <a className="dropdown-item" href="#">Settings 1</a>
                    <a className="dropdown-item" href="#">Settings 2</a>
                    </div>
                </li>
                <li><a className="close-link"><i className="fa fa-close"></i></a>
                </li> */}
            </ul>
            <div className="clearfix"></div>
            </div>
            <div className="x_content">
            {/* <table className="table table-hover">
                <thead>
                <tr>
                    <th>#</th>
                    <th>type</th>
                    <th>location</th>
                    <th>Station</th>
                    <th>Officer</th>
                    <th>status</th>
                    <th>Date</th>
                </tr>
                </thead>
                <tbody>
                {resources.map(item => (
                    <tr key={item.id} onClick={(e) => getResource(item.id, item.module, e)}>
                      <th scope="row">{item.id}</th>
                      <td>{item.module}</td>
                      <td>{item.location}</td>
                      <td>{item.police_station.name}</td>
                      <td>{item.police_officer.service_number}</td>
                      <td><span className={`badge badge-${item.is_closed ? 'primary' : 'danger'}`}>{item.is_closed ? 'closed' : 'pending'}</span></td>
                      <td>{item.posted_date}</td>
                    </tr>
                ))}
                </tbody>
            </table> */}
            <table className="table table-hover">
                <thead>
                <tr>
                    <th>#</th>
                    <th>Category</th>
                    <th>Reporter Name/ID No</th>
                    <th>OB Number</th>
                </tr>
                </thead>
                <tbody>
                {resources.map(item => (
                    <tr key={item.id} onClick={(e) => getResource(item.id, item.module, e)}>
                      <th scope="row">{item.id}</th>
                      <td>
                        {item.details.length
                        ? item.details.map(item => (
                            `${item.category.name} `
                        ))
                        : '-'
                        }
                      </td>
                      <td>
                        {item.reporters.length 
                          ? <Reporters reporters={item.reporters} />
                          : '-'
                        }
                      </td>
                      <td>{item.ob_no ? item.ob_no : "-"}</td>
                    </tr>
                ))}
                </tbody>
            </table>

            </div>
        </div>
      </div>
    </div>
  );
}