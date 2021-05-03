import { HttpClient, HttpInterceptor, HttpRequest, HttpHandler, HttpEvent, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import jwt_decode from 'jwt-decode';
import * as moment from 'moment';
import { tap, shareReplay } from 'rxjs/operators';
//import { Credentials } from 'crypto';
export interface Credentials {
  // Customize received credentials here
  user_id: string;

  username: string;
  exp: number;
  //token: string;
}
interface JWTPayload {
  user_id: number;
  username: string;
  email: string;
  exp: number;
}
export interface LoginContext {
  username: string;
  password: string;
  remember?: boolean;
}

const credentialsKey = 'credentials';

/**
 * Provides a base for authentication workflow.
 * The Credentials interface as well as login/logout methods should be replaced with proper implementation.
 */
@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    const token = localStorage.getItem('token');

    if (token) {
      const cloned = req.clone({
        headers: req.headers.set('Authorization', 'JWT '.concat(token)),
      });

      return next.handle(cloned);
    } else {
      return next.handle(req);
    }
  }
}
@Injectable()
export class AuthenticationService {
  private _credentials: Credentials | null;
  private httpOptions: any;
  constructor(private httpClient: HttpClient) {
    const savedCredentials = sessionStorage.getItem(credentialsKey) || localStorage.getItem(credentialsKey);

    if (savedCredentials) {
      this._credentials = JSON.parse(savedCredentials);
    }

    this.httpOptions = {
      headers: new HttpHeaders({ 'Content-Type': 'application/json' }),
    };
  }
  public setSession(authResult: any) {
    const token = authResult.token;
    const payload = <Credentials>jwt_decode(token);
    console.log(payload.username);
    const expiresAt = moment.unix(payload.exp);
    console.log('payload is');
    console.log(payload);
    console.log('------------end---------');
    console.log(payload.user_id);
    console.log(expiresAt);
    console.log(payload.user_id);

    localStorage.setItem('token', authResult.token);
    localStorage.setItem('id', payload.user_id);
    localStorage.setItem('username', payload.username);
    localStorage.setItem('expires_at', JSON.stringify(expiresAt.valueOf()));
  }
  private baseUrl = 'http://localhost:5000/api/user';
  /**
   * Authenticates the user.
   * @param context The login parameters.
   * @return The user credentials.
   */
  login(context: LoginContext): Observable<object> {
    // Replace by proper authentication call
    /*const header = new Headers();
     header.append('Content-Type', 'application/x-www-form-urlencoded');
     const options = new RequestOptions({ headers: header });*/
    let headers = new HttpHeaders({
      'Content-Type': 'application/json',
    });
    let options = {
      headers: headers,
    };
    let temp;
    console.log(context);
    const dataContext = {
      username: context.username,
      password: context.password,
    };
    console.log(`${this.baseUrl}/api/user/login`);
    return this.httpClient.post(`${this.baseUrl}/login/`, JSON.stringify(dataContext), options);

    //return this.httpClient.post('/api/login/', JSON.stringify(dataContext), this.httpOptions)
  }

  /**
   * Logs out the user and clear credentials.
   * @return True if the user was logged out successfully.
   */
  logout(): Observable<boolean> {
    // Customize credentials invalidation here
    this.setCredentials();
    return of(true);
  }

  /**
   * Checks is the user is authenticated.
   * @return True if the user is authenticated.
   */
  isAuthenticated(): boolean {
    return !!this.credentials;
  }
  getExpiration() {
    const expiration = localStorage.getItem('expires_at');
    const expiresAt = JSON.parse(expiration);

    return moment(expiresAt);
  }

  isLoggedIn() {
    console.log(this.getExpiration());
    return moment().isBefore(this.getExpiration());
  }

  isLoggedOut() {
    return !this.isLoggedIn();
  }

  /**
   * Gets the user credentials.
   * @return The user credentials or null if the user is not authenticated.
   */
  get credentials(): string | null {
    if (localStorage.getItem('username') != null) return localStorage.getItem('username');
    var payload = <Credentials>jwt_decode(localStorage.getItem('token'));
    if (payload == null) return 'abc';
  }
  /*get credentials(): string {
    //return localStorage.getItem(credentialsKey);
    return this._credentials.username;
  }*/
  /**
   * Sets the user credentials.
   * The credentials may be persisted across sessions by setting the `remember` parameter to true.
   * Otherwise, the credentials are only persisted for the current session.
   * @param credentials The user credentials.
   * @param remember True to remember credentials across sessions.
   */
  public setCredentials(credentials?: Credentials, remember?: boolean) {
    this._credentials = credentials || null;

    if (credentials) {
      const storage = remember ? localStorage : sessionStorage;
      storage.setItem(credentialsKey, JSON.stringify(credentials));
    } else {
      sessionStorage.removeItem(credentialsKey);
      localStorage.removeItem(credentialsKey);
    }
    localStorage.removeItem('token');
    localStorage.removeItem('expires_at');
    localStorage.removeItem('username');
    localStorage.removeItem('id');
  }

  refreshToken() {
    if (moment().isBetween(this.getExpiration().subtract(1, 'days'), this.getExpiration())) {
      return this.httpClient
        .post(this.baseUrl.concat('/token/refresh-token/'), { token: this.credentials })
        .pipe(
          tap((response) => this.setSession(response)),
          shareReplay()
        )
        .subscribe();
    }
  }
}
