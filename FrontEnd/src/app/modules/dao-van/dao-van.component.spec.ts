import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DaoVanComponent } from './dao-van.component';

describe('DaoVanComponent', () => {
  let component: DaoVanComponent;
  let fixture: ComponentFixture<DaoVanComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [DaoVanComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DaoVanComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
