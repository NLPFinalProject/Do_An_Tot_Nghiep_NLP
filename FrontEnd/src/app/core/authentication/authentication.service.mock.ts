import { Observable, of } from 'rxjs';

import { Credentials, LoginContext } from './authentication.service';

export class MockAuthenticationService {
  credentials: Credentials | null = {
    username: 'test',
    exp: 1,
    user_id: '12',
    // token: '123'
  };

  login(context: LoginContext): Observable<Credentials> {
    console.log('wwwwwww');
    return of({
      username: context.username,
      exp: 1,
      user_id: '1',
      // token: '123456'
    });
  }

  logout(): Observable<boolean> {
    this.credentials = null;
    return of(true);
  }

  isAuthenticated(): boolean {
    return !!this.credentials;
  }
}
