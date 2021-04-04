import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { RoutingService } from '@app/core/services/Routing/routing.services';
import { RoutingBlog } from '../../commons/routing.constant';

@Component({
  selector: 'app-page-blog-index',
  templateUrl: './page-blog-index.component.html',
  styleUrls: ['./page-blog-index.component.scss']
})
export class PageBlogIndexComponent implements OnInit {
  blogs: any;
  constructor(private routingService: RoutingService) {}

  ngOnInit() {
    this.getBlog();
  }

  routingDetail(id: any) {
    this.routingService.navigateToUpdate(RoutingBlog.Blog, id);
  }

  getBlog() {
    this.blogs = [
      {
        title: 'Title 1',
        description:
          'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and       scrambled it to make a type specimen book. '
      },
      {
        title: 'Title 2',
        description:
          'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and       scrambled it to make a type specimen book. '
      },
      {
        title: 'Title 3',
        description:
          'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and       scrambled it to make a type specimen book. '
      },
      {
        title: 'Title 4',
        description:
          'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and       scrambled it to make a type specimen book. '
      },
      {
        title: 'Title 5',
        description:
          'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and       scrambled it to make a type specimen book. '
      },
      {
        title: 'Title 6',
        description:
          'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and       scrambled it to make a type specimen book. '
      },
      {
        title: 'Title 7',
        description:
          'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and       scrambled it to make a type specimen book. '
      },
      {
        title: 'Title 8',
        description:
          'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and       scrambled it to make a type specimen book. '
      }
    ];
  }
}
