import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, of } from 'rxjs';

//import{User} from '@../../../src/app/login/User'

@Injectable({
  providedIn: 'root',
})
export class UserService {
  private baseUrl = 'http://localhost:5000/api/user';

  private params: HttpParams;
  constructor(private http: HttpClient) {
    this.params = new HttpParams();
  }
  getSession(id: string): Observable<Object> {
    let params = new HttpParams().set('id', id);

    console.log(params.toString());
    return this.http.get(`${this.baseUrl}/session`, { params: params });
  }
  register(user: Object): Observable<Object> {
    return this.http.post(`${this.baseUrl}/register`, user);
  }
  isAdmin(username: string): Observable<Object> {
    let params = new HttpParams().set('username', username);

    console.log(username);
    return this.http.get(`${this.baseUrl}/is-admin-user/`, { params: params });
  }
  refreshToken(): Observable<Object> {
    let token = localStorage.getItem('token');
    return this.http.post(`${this.baseUrl}/refresh-token/`, token);
  }
  lockUser(data: string): Observable<Object> {
    let params = new HttpParams().set('username', data);
    //params.set("isAdmin",localStorage.getItem('isAdmin'));
    //console.log(username);
    return this.http.get(`${this.baseUrl}/lock-user`, { params: params });
  }
  unlockUser(data: string): Observable<Object> {
    let params = new HttpParams().set('username', data);
    //params.set("isAdmin",localStorage.getItem('isAdmin'));
    //console.log(username);
    return this.http.get(`${this.baseUrl}/unlock-user`, { params: params });
  }
  getUserList(data: any): Observable<Object> {
    let params = new HttpParams().set('isAdmin', localStorage.getItem('isAdmin'));
    //params.set("isAdmin",localStorage.getItem('isAdmin'));
    //console.log(username);
    return this.http.get(`${this.baseUrl}/get-user-list`, { params: params });
  }
  ActivateUser(user: Object): Observable<Object> {
    return this.http.post(`${this.baseUrl}/activate`, user);
  }

  createUSer(user: Object): Observable<Object> {
    return this.http.post(`${this.baseUrl}/api/`, user);
  }
  updateUSer(user: Object): Observable<Object> {
    return this.http.post(`${this.baseUrl}/api/update-user`, user);
  }

  login(user: Object): Observable<Object> {
    console.log(`${this.baseUrl}/api/login`);
    return this.http.post(`${this.baseUrl}/login`, user);
  }
  profile(id: string): Observable<Object> {
    //this.params.set('username',id);
    //console.log(id);

    let params = new HttpParams().set('username', id);

    console.log(params.toString());
    return this.http.get(`${this.baseUrl}/profile/`, { params: params });
  }

  ForgotPassword(user: Object): Observable<Object> {
    return this.http.post(`${this.baseUrl}/forgot-password`, user);
  }

  ResetPassword(user: Object): Observable<Object> {
    return this.http.post(`${this.baseUrl}/reset-password`, user);
  }
  /*register(user: Object): Observable<Object> {
    return this.http.post('/api/SendMail',user);
  }

  ActivateUser(user: Object): Observable<Object> {
    return this.http.post('/api/activate',user);
  }

  createUSer(user: Object): Observable<Object> {
    return this.http.post('api/', user);
  }

  login(user: Object): Observable<Object> {
    return this.http.post('api/login',user);
  }

  ForgotPassword(user: Object): Observable<Object> {
    return this.http.post('/api/forgot-password',user);
  }

  ResetPassword(user: Object): Observable<Object> {
    return this.http.post('/api/reset-password',user);
  }*/
}
