import { Component, OnInit } from '@angular/core';
import { Title } from '@angular/platform-browser';
import { ActivatedRoute, NavigationEnd, Router } from '@angular/router';
import { Logger } from '@app/core';
import { filter, map, mergeMap } from 'rxjs/operators';

const log = new Logger('App');

@Component({
  selector: 'app-breadcrumb',
  templateUrl: './breadcrumb.component.html',
  styleUrls: ['./breadcrumb.component.scss']
})
export class BreadcrumbComponent implements OnInit {
  pageInfo: any;
  constructor(private router: Router, private activatedRoute: ActivatedRoute, private titleService: Title) {
    this.getPageInfo();
  }
  ngOnInit() {}

  getPageInfo(): void {
    this.router.events
      .pipe(filter(event => event instanceof NavigationEnd))
      .pipe(map(() => this.activatedRoute))
      .pipe(
        map(route => {
          while (route.firstChild) {
            route = route.firstChild;
          }
          return route;
        })
      )
      .pipe(filter(route => route.outlet === 'primary'))
      .pipe(mergeMap(route => route.data))
      .subscribe(event => {
        this.pageInfo = event;
        console.log(this.pageInfo);
      });
  }
}
