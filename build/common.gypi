# Copyright 2009 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

{
  'variables': {
    'variables': {
      'clang%': 0,
      'conditions': [
        ['OS=="mac"', {
          'clang%': 1,
        }],
      ],
    },
    'clang%': '<(clang)',
  },

  'target_defaults': {
    'includes': [
      'filename_rules.gypi',
    ],
    'conditions': [

      ['OS=="mac"', {
        'xcode_settings': {
          'ALWAYS_SEARCH_USER_PATHS': 'NO',
          'GCC_C_LANGUAGE_STANDARD': 'c99',         # -std=c99
          'GCC_CW_ASM_SYNTAX': 'NO',                # No -fasm-blocks
          'GCC_DYNAMIC_NO_PIC': 'NO',               # No -mdynamic-no-pic
          'GCC_ENABLE_CPP_EXCEPTIONS': 'NO',        # -fno-exceptions
          'GCC_ENABLE_CPP_RTTI': 'NO',              # -fno-rtti
          'GCC_ENABLE_PASCAL_STRINGS': 'NO',        # No -mpascal-strings

          # GCC_INLINES_ARE_PRIVATE_EXTERN maps to -fvisibility-inlines-hidden
          'GCC_INLINES_ARE_PRIVATE_EXTERN': 'YES',

          'GCC_OBJC_CALL_CXX_CDTORS': 'YES',        # -fobjc-call-cxx-cdtors
          'GCC_PRECOMPILE_PREFIX_HEADER': 'NO',
          'GCC_SYMBOLS_PRIVATE_EXTERN': 'YES',      # -fvisibility=hidden
          'GCC_THREADSAFE_STATICS': 'NO',           # -fno-threadsafe-statics
          'GCC_TREAT_WARNINGS_AS_ERRORS': 'YES',    # -Werror
          'GCC_WARN_ABOUT_MISSING_NEWLINE': 'YES',  # -Wnewline-eof
          'OTHER_CFLAGS': [
            '-fno-strict-aliasing',   # See http://crbug.com/32204
            '-fstack-protector-all',  # Implies -fstack-protector
          ],
          'USE_HEADERMAP': 'NO',
          'WARNING_CFLAGS': [
            '-Wall',
            '-Wendif-labels',
            '-Wextra',

            # Don't warn about unused function parameters.
            '-Wno-unused-parameter',

            # Don't warn about the "struct foo f = {0};" initialization
            # pattern.
            '-Wno-missing-field-initializers',
          ],

          'conditions': [
            ['clang!=0', {
              # Don't link in libarclite_macosx.a, see http://crbug.com/156530.
              'CLANG_LINK_OBJC_RUNTIME': 'NO',      # -fno-objc-link-runtime

              'CLANG_WARN_CXX0X_EXTENSIONS': 'NO',  # -Wno-c++0x-extensions
              'GCC_VERSION': 'com.apple.compilers.llvm.clang.1_0',
              'WARNING_CFLAGS': [
                '-Wheader-hygiene',
                '-Wno-c++11-extensions',
                '-Wno-char-subscripts',
                '-Wno-covered-switch-default',
                '-Wno-unnamed-type-template-args',
                '-Wno-unused-function',
              ],
            }, {  # else: clang==0
              'GCC_VERSION': '4.2',
            }],
          ],

          'target_conditions': [
            ['_type=="executable"', {
              'OTHER_LDFLAGS': [
                '-Wl,-pie',  # Position-independent executable (MH_PIE)
              ],
            }],
          ],

        },
      }],

      ['OS=="linux"', {
        'cflags': [
          '-fPIC',
          '-fno-exceptions',
          '-fno-strict-aliasing',   # See http://crbug.com/32204
          '-fstack-protector-all',  # Implies -fstack-protector
          '-fvisibility=hidden',
          '-g',
          '-pipe',
          '-pthread',
          '-Wall',
          '-Werror',
          '-Wextra',
          '-Wno-unused-parameter',
          '-Wno-missing-field-initializers',
        ],
        'cflags_cc': [
          '-fno-rtti',
          '-fno-threadsafe-statics',
          '-fvisibility-inlines-hidden',
          '-Wsign-compare',
        ],
        'defines': [
          '_FILE_OFFSET_BITS=64',
        ],
        'ldflags': [
          '-fPIC',
          '-pthread',
          '-Wl,--as-needed',
          '-Wl,-z,noexecstack',
        ],

        'conditions': [
          ['clang!=0', {
            'cflags': [
              '-Wheader-hygiene',
              '-Wno-c++11-extensions',
              '-Wno-char-subscripts',
              '-Wno-covered-switch-default',
              '-Wno-unnamed-type-template-args',
              '-Wno-unused-function',
            ],
          }, {  # else: clang==0
            'cflags': [
              '-mfpmath=sse',
            ],
          }],
        ],

      }],

    ],
    'default_configuration': 'Debug',
    'configurations': {
      'Release': {
        'defines': [
          'NDEBUG',
        ],
        'conditions': [

          ['OS=="mac"', {
            'xcode_settings': {
              'DEAD_CODE_STRIPPING': 'YES',  # -Wl,-dead_strip
              'DEBUG_INFORMATION_FORMAT': 'dwarf-with-dsym',
              'GCC_OPTIMIZATION_LEVEL': '3',

              'target_conditions': [
                ['_type=="executable" or _type=="shared_library" or \
                  _type=="loadable_module"', {
                  'DEPLOYMENT_POSTPROCESSING': 'YES',
                  'STRIP_INSTALLED_PRODUCT': 'YES',
                }],
                ['_type=="shared_library" or _type=="loadable_module"', {
                  'STRIPFLAGS': '-x',
                }],
              ],

            },
          }],

          ['OS=="linux"', {
            'cflags': [
              '-O3',
              '-fdata-sections',
              '-ffunction-sections',
            ],
            'ldflags': [
              '-Wl,-O1',
              '-Wl,--gc-sections',
            ],

            'conditions': [
              ['clang==0', {
                'cflags': [
                  '-fno-ident',
                ],
              }],
            ],

          }],

        ],
      },
      'Debug': {
        'conditions': [

          ['OS=="mac"', {
            'xcode_settings': {
              'COPY_PHASE_STRIP': 'NO',
              'DEBUG_INFORMATION_FORMAT': 'dwarf',
              'GCC_OPTIMIZATION_LEVEL': '0',
            },
          }],

          ['OS=="linux"', {
            'cflags': [
              '-O0',
            ],
          }],

        ],
      },
    },
  },

  'conditions': [
    ['OS=="mac"', {
      'xcode_settings': {
        'SYMROOT': '<(DEPTH)/xcodebuild',
      },
    }],
  ],
}
