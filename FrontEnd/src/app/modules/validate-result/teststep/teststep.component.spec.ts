import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TeststepComponent } from './teststep.component';

describe('TeststepComponent', () => {
  let component: TeststepComponent;
  let fixture: ComponentFixture<TeststepComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [TeststepComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TeststepComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
