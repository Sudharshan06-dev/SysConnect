import { ApplicationConfig, provideZoneChangeDetection } from '@angular/core';
import {provideRouter, withInMemoryScrolling, withViewTransitions} from '@angular/router';

import { routes } from './app.routes';
import {provideAnimations} from '@angular/platform-browser/animations';
import {provideHttpClient, withInterceptors} from '@angular/common/http';
import {spinnerInterceptor} from '../interceptors/spinner.interceptor';
import {authInterceptor} from '../interceptors/auth.interceptor';
import {provideToastr} from 'ngx-toastr';
import {TOAST_CONFIGURATION} from '../environment';

export const appConfig: ApplicationConfig = {
  providers: [
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideRouter(routes,  withViewTransitions(),
      withInMemoryScrolling({
        anchorScrolling: 'enabled',
        scrollPositionRestoration: 'enabled'
      })),
    provideAnimations(),
    provideHttpClient(withInterceptors([spinnerInterceptor, authInterceptor])),
    provideToastr(TOAST_CONFIGURATION),
  ]
};
