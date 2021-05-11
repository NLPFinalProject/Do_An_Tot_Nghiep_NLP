import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { PageBlogIndexComponent } from './page-blog-index.component';

describe('PageBlogIndexComponent', () => {
  let component: PageBlogIndexComponent;
  let fixture: ComponentFixture<PageBlogIndexComponent>;

  beforeEach(
    waitForAsync(() => {
      TestBed.configureTestingModule({
        declarations: [PageBlogIndexComponent],
      }).compileComponents();
    })
  );

  beforeEach(() => {
    fixture = TestBed.createComponent(PageBlogIndexComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
