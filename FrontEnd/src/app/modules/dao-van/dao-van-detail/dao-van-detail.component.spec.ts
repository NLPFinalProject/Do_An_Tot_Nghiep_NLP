import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { DaoVanDetailComponent } from './dao-van-detail.component';

describe('DaoVanDetailComponent', () => {
  let component: DaoVanDetailComponent;
  let fixture: ComponentFixture<DaoVanDetailComponent>;

  beforeEach(
    waitForAsync(() => {
      TestBed.configureTestingModule({
        declarations: [DaoVanDetailComponent],
      }).compileComponents();
    })
  );

  beforeEach(() => {
    fixture = TestBed.createComponent(DaoVanDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
