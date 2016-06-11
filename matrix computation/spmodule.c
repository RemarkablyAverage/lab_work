#include <Python.h>
#include "structmember.h"
#include <assert.h>

/* Kyle's implementation */

// like [(2, 3.0), (4, 6.2), (7, 1.0)]
typedef struct SpRow {
  size_t nz;
  size_t maxnz;
  double *values;
  size_t *cols; // in increasing order
} SpRow;

static void SpRow_init(SpRow *row, size_t initsize) {
  assert(initsize > 0);
  row->nz = 0;
  row->maxnz = initsize;
  row->values = malloc(sizeof(double) * initsize);
  row->cols = malloc(sizeof(size_t) * initsize);
}
static void SpRow_free(SpRow *row) {
  free(row->values);
  free(row->cols);
}
static void SpRow_ensure_capacity(SpRow *row, size_t capacity) {
  if (capacity > row->maxnz) {
    size_t newsize = row->maxnz * 2;
    while (capacity > newsize) {
      newsize *= 2;
    }
    double *new_values = malloc(sizeof(double) * newsize);
    size_t *new_cols = malloc(sizeof(size_t) * newsize);
    memcpy(new_values, row->values, sizeof(double) * row->nz);
    memcpy(new_cols, row->cols, sizeof(size_t) * row->nz);
    free(row->values);
    free(row->cols);
    row->values = new_values;
    row->cols = new_cols;
    row->maxnz = newsize;
  }
}
static void SpRow_append(SpRow *row, size_t j, double value) {
  SpRow_ensure_capacity(row, row->nz + 1);
  row->values[row->nz] = value;
  row->cols[row->nz] = j;
  row->nz++;
}
static void SpRow_insert(SpRow *row, size_t j, double value) {
  if (row->nz == 0 || row->cols[row->nz-1] < j) {
    SpRow_append(row, j, value);
    return;
  }
  size_t lo, hi;
  lo = 0;
  hi = row->nz;
  while (lo < hi) {
    size_t mid = lo + (hi - lo) / 2;
    size_t col = row->cols[mid];
    if (col == j) {
      // then replace
      row->values[mid] = value;
      return;
    } else if (col < j) {
      lo = mid + 1;
    } else /* col > j */ {
      hi = mid;
    }
  }
  assert(lo != row->nz);
  // lo is now index of first element whose column is >= j
  SpRow_ensure_capacity(row, row->nz + 1);
  for (size_t k = 0; k < row->nz - lo; k++) {
    row->values[row->nz - k] = row->values[row->nz - k - 1];
    row->cols[row->nz - k] = row->cols[row->nz - k - 1];
  }
  row->values[lo] = value;
  row->cols[lo] = j;
  row->nz++;
}
static double SpRow_get(SpRow *row, size_t j) {
  size_t lo, hi;
  lo = 0;
  hi = row->nz;
  while (lo < hi) {
    size_t mid = lo + (hi - lo) / 2;
    size_t col = row->cols[mid];
    if (col == j) {
      return row->values[mid];
    } else if (col < j) {
      lo = mid + 1;
    } else /* col > j */ {
      hi = mid;
    }
  }
  return 0.0;
}

static double SpRow_l1_diff(SpRow *r1, SpRow *r2) {
  double norm = 0.0;
  size_t i, j;
  i = 0; j = 0;
  while (i < r1->nz && j < r2->nz) {
    if (r1->cols[i] == r2->cols[j]) {
      norm += abs(r1->values[i] - r2->values[j]);
      i++; j++;
    } else if (r1->cols[i] < r2->cols[j]) {
      norm += abs(r1->values[i]);
      i++;
    } else /* r1->cols[i] > r2->cols[j] */ {
      norm += abs(r2->values[j]);
      j++;
    }
  }
  while (i < r1->nz) {
    norm += abs(r1->values[i]);
    i++;
  }
  while (j < r2->nz) {
    norm += abs(r2->values[j]);
    j++;
  }
  return norm;
}

/*static void SpRow_debug_print(SpRow *row) {
  printf("[");
  for (size_t i = 0; i < row->nz; i++) {
    printf("(%zu,%f),", row->cols[i], row->values[i]);
  }
  printf("]\n");
  }*/

typedef struct SpMatrix {
  size_t nrows;
  size_t ncols;
  SpRow *rows;
} SpMatrix;

static void SpMatrix_init(SpMatrix *matrix, size_t nrows, size_t ncols, size_t initsize) {
  matrix->rows = malloc(nrows * sizeof(SpRow));
  for (size_t i = 0; i < nrows; i++) {
    SpRow_init(&matrix->rows[i], initsize);
  }
  matrix->nrows = nrows;
  matrix->ncols = ncols;
}
static void SpMatrix_free(SpMatrix *matrix) {
  if (matrix->rows == NULL) {
    return;
  }
  for (size_t i = 0; i < matrix->nrows; i++) {
    SpRow_free(&matrix->rows[i]);
  }
  free(matrix->rows);
  matrix->rows = NULL;
}
static void SpMatrix_insert(SpMatrix *matrix, size_t i, size_t j, double value) {
  if (i < matrix->nrows && j < matrix->ncols) {
    SpRow_insert(&matrix->rows[i], j, value);
  }
}
static double SpMatrix_get(SpMatrix *matrix, size_t i, size_t j) {
  if (i < matrix->nrows)
    return SpRow_get(&matrix->rows[i], j);
  else
    return 0.0;
}
/*static void SpMatrix_debug_print(SpMatrix *matrix) {
  for (size_t i = 0; i < matrix->nrows; i++) {
    SpRow_debug_print(&matrix->rows[i]);
  }
  }*/

static double SpMatrix_l1_diff(SpMatrix *m1, SpMatrix *m2) {
  assert(m1->nrows == m2->nrows && m1->ncols == m2->ncols);
  double norm = 0.0;
  for (size_t i = 0; i < m1->nrows; i++) {
    norm += SpRow_l1_diff(&m1->rows[i], &m2->rows[i]);
  }
  return norm;
}
 

static PyObject *SpamError;

typedef struct {
    PyObject_HEAD
    SpMatrix mat;
} sp_spmatrix_Object;

static void sp_spmatrix_dealloc(sp_spmatrix_Object *self) {
  SpMatrix_free(&self->mat);
}
static PyObject *sp_spmatrix_new(PyTypeObject *type, PyObject *args, PyObject *kwds) {
  sp_spmatrix_Object *self;
  self = (sp_spmatrix_Object *)type->tp_alloc(type, 0);
  if (self != NULL) {
    self->mat.rows = NULL;
  }
  return (PyObject *)self;
}
static int sp_spmatrix_init(sp_spmatrix_Object *self, PyObject *args, PyObject *kwds) {
  static char *kwlist[] = {"nrows", "ncols", "initsize", NULL};
  int nrows;
  int ncols;
  int initsize = 4;
  if (!PyArg_ParseTupleAndKeywords(args, kwds, "ii|i", kwlist,
                                   &nrows, &ncols, &initsize))
    return -1;
  SpMatrix_init(&self->mat, nrows, ncols, initsize);
  return 0;
}

static PyObject *sp_spmatrix_print_dense(PyObject *_self, PyObject *args) {
  sp_spmatrix_Object *self = (sp_spmatrix_Object *)_self;
  printf("[");
  for (size_t i = 0; i < self->mat.nrows; i++) {
    if (i > 0)
      printf(",\n ");
    printf("[");
    for (size_t j = 0; j < self->mat.ncols; j++) {
      if (j > 0)
        printf(",");
      printf("% 12lf", SpMatrix_get(&self->mat, i, j));
    }
    printf("]");
  }
  printf("]\n");
  Py_INCREF(Py_None);
  return Py_None;
}

static PyMethodDef sp_spmatrix_methods[] = {
  {"print_dense", sp_spmatrix_print_dense, METH_NOARGS,
   "Prints out a dense representation of the matrix."},
  {NULL}  /* Sentinel */
};

static PyMemberDef sp_spmatrix_members[] = {
  {"nrows", T_INT, offsetof(sp_spmatrix_Object, mat) + offsetof(SpMatrix, nrows),
   READONLY, "Number of rows in the matrix"},
  {"ncols", T_INT, offsetof(sp_spmatrix_Object, mat) + offsetof(SpMatrix, ncols),
   READONLY, "Number of columns in the matrix"},
  {NULL} /* Sentinel */
};

static PyObject *sp_spmatrix_subscript(PyObject *o, PyObject *key) {
  int i, j;
  if (!PyArg_ParseTuple(key, "ii", &i, &j))
    return NULL;
  sp_spmatrix_Object *self = (sp_spmatrix_Object *)o;
  if (i < self->mat.nrows && j < self->mat.ncols) {
    return PyFloat_FromDouble(SpMatrix_get(&self->mat, i, j));
  } else {
    PyErr_SetString(PyExc_IndexError, "index out of bounds");
    return NULL;
  }
}
static int sp_spmatrix_ass_subscript(PyObject *o, PyObject *key, PyObject *v) {
  int i, j;
  if (!PyArg_ParseTuple(key, "ii", &i, &j))
    return -1;
  sp_spmatrix_Object *self = (sp_spmatrix_Object *)o;
  if (i < self->mat.nrows && j < self->mat.ncols) {
    float val;
    if (PyFloat_Check(v)) {
      val = PyFloat_AS_DOUBLE(v);
    } else if (PyInt_Check(v)) {
      val = PyInt_AS_LONG(v);
    } else {
      PyErr_SetString(PyExc_TypeError, "parameter must be a float or integer");
      return -1;
    }
    SpMatrix_insert(&self->mat, i, j, val);
    return 0;
  } else {
    PyErr_SetString(PyExc_IndexError, "index out of bounds");
    return -1;
  }
}

static PyMappingMethods sp_spmatrix_mapping = {
  NULL, /*mp_length*/
  sp_spmatrix_subscript, /*mp_subscript*/
  sp_spmatrix_ass_subscript, /*mp_ass_subscript*/
};

static PyTypeObject sp_spmatrix_Type = {
    PyObject_HEAD_INIT(NULL)
    0,                         /*ob_size*/
    "spam.SpMatrix",             /*tp_name*/
    sizeof(sp_spmatrix_Object), /*tp_basicsize*/
    0,                         /*tp_itemsize*/
    (destructor)sp_spmatrix_dealloc,                         /*tp_dealloc*/
    0,                         /*tp_print*/
    0,                         /*tp_getattr*/
    0,                         /*tp_setattr*/
    0,                         /*tp_compare*/
    0,                         /*tp_repr*/
    0,                         /*tp_as_number*/
    0,                         /*tp_as_sequence*/
    &sp_spmatrix_mapping,                         /*tp_as_mapping*/
    0,                         /*tp_hash */
    0,                         /*tp_call*/
    0,                         /*tp_str*/
    0,                         /*tp_getattro*/
    0,                         /*tp_setattro*/
    0,                         /*tp_as_buffer*/
    Py_TPFLAGS_DEFAULT,        /*tp_flags*/
    "Sparse matrices",           /* tp_doc */
    0,		               /* tp_traverse */
    0,		               /* tp_clear */
    0,		               /* tp_richcompare */
    0,		               /* tp_weaklistoffset */
    0,		               /* tp_iter */
    0,		               /* tp_iternext */
    sp_spmatrix_methods,             /* tp_methods */
    sp_spmatrix_members,             /* tp_members */
    0,           /* tp_getset */
    0,                         /* tp_base */
    0,                         /* tp_dict */
    0,                         /* tp_descr_get */
    0,                         /* tp_descr_set */
    0,                         /* tp_dictoffset */
    (initproc)sp_spmatrix_init,      /* tp_init */
    0,                         /* tp_alloc */
    sp_spmatrix_new,                 /* tp_new */
};


static PyObject *sp_l1_diff(PyObject *self, PyObject *args) {
  sp_spmatrix_Object *o1, *o2;

  if (!PyArg_ParseTuple(args, "O!O!",
                        &sp_spmatrix_Type, &o1,
                        &sp_spmatrix_Type, &o2))
    return NULL;
  if (o1->mat.nrows != o2->mat.nrows
      || o1->mat.ncols != o2->mat.ncols) {
    PyErr_SetString(PyExc_TypeError, "matrix dimensions do not match");
    return NULL;
  }
  return PyFloat_FromDouble(SpMatrix_l1_diff(&o1->mat, &o2->mat));
}

static PyMethodDef SpamMethods[] = {
    {"l1_diff",  sp_l1_diff, METH_VARARGS,
     "Computes the L1 difference between two sparse matrices."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};


PyMODINIT_FUNC initspam(void) {
  PyObject *m;
  m = Py_InitModule("spam", SpamMethods);
  if (m == NULL)
    return;

  sp_spmatrix_Type.tp_new = PyType_GenericNew;
  if (PyType_Ready(&sp_spmatrix_Type) < 0)
    return;

  Py_INCREF(&sp_spmatrix_Type);
  PyModule_AddObject(m, "SpMatrix", (PyObject *)&sp_spmatrix_Type);

  //  SpMatrix_init(&mat, 5, 5, 10);
  
  SpamError = PyErr_NewException("spam.error", NULL, NULL);
  Py_INCREF(SpamError);
  PyModule_AddObject(m, "error", SpamError);
}
