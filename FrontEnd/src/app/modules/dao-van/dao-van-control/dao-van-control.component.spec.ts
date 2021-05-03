import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DaoVanControlComponent } from './dao-van-control.component';

describe('DaoVanControlComponent', () => {
  let component: DaoVanControlComponent;
  let fixture: ComponentFixture<DaoVanControlComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [DaoVanControlComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DaoVanControlComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
