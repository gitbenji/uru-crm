import * as gulp from 'gulp';
import {runSequence, task} from './tools/utils';
import {join} from 'path';

// --------------
// Clean (override).

gulp.task('clean',       task('clean', 'all'));
gulp.task('clean.dist',  task('clean', 'dist'));
gulp.task('clean.test',  task('clean', 'test'));
gulp.task('clean.tmp',   task('clean', 'tmp'));
gulp.task('check.versions', task('check.versions'));


// --------------
// Postinstall.
gulp.task('postinstall', done =>
  runSequence('clean',
              'npm',
              done));

// --------------
// Build dev.
gulp.task('build.dev', done =>
  runSequence('clean.dist',
              'tslint',
              'build.sass.dev',
              'build.assets.dev',
              'build.js.dev',
              'build.index.dev',
              done));

// --------------
// Build prod.
gulp.task('build.prod', done =>
  runSequence('clean.dist',
              'clean.tmp',
              'tslint',
              'build.sass.prod',
              'build.assets.prod',
              'build.html_css.prod',
              'build.js.prod',
              'build.bundles',
              'build.index.prod',
              done));

// --------------
// Serve.
gulp.task('serve', done =>
  runSequence('build.dev',
              'server.start',
              'watch.serve',
              done));

