#define PY_SSIZE_T_CLEAN

#include <Python.h>
#include <string.h>

typedef struct
{
    char *c;
    int len;
    int capacity;

} arr_t;

void arr_init(arr_t *arr)
{
    arr->c = NULL;

    arr->len = 0;
    arr->capacity = 0;
}

int arr_append(arr_t *arr, char c)
{
    if (arr->capacity == 0)
    {
        arr->c = malloc(2 * sizeof(char));
        if (arr->c == NULL)
            return 1;
        arr->capacity = 2;
    }

    if (arr->len + 1 > arr->capacity)
    {
        arr->c = realloc(arr->c, arr->capacity * 2);
        if (arr->c == NULL)
            return 1;
        arr->capacity *= 2;
    }

    arr->c[arr->len] = c;
    ++arr->len;

    return 0;
}

int arr_append_seq(arr_t *arr, const char *seq)
{
    for (const char *c = seq; *c != '\0'; c++)
        if (arr_append(arr, *c))
            return 1;

    return 0;
}

void arr_free(arr_t *arr)
{
    free(arr->c);
    arr->c = NULL;

    arr->capacity = 0;
    arr->len = 0;
}

int is_valid_str(const char *str)
{
    if (*str != '"')
        return 0;
    else
        ++str;

    int key_len = 0;
    while (isprint(*str) && *str != '"')
    {
        ++str;
        ++key_len;
    }

    if (key_len == 0)
        return 0;

    if (*str != '"')
        return 0;
    else
        ++str;

    return key_len + 2;
}

int is_valid_num(const char *str)
{
    int key_len = 0;

    if (*str == '-')
    {
        ++key_len;
        ++str;
    }

    while (isdigit(*str))
    {
        ++str;
        ++key_len;
    }

    if (key_len == 0)
        return 0;

    return key_len;
}

int is_json_valid(const char *json)
{
    if (json[0] != '{' || json[strlen(json) - 1] != '}')
        return 0;

    if (strlen(json) == 2)
        return 1;

    int commas_count = 0;
    int kv_count = 0;

    ++json;
    while (*json != '}')
    {
        int str_len = is_valid_str(json);
        if (str_len == 0)
            return 0;
        else
            json += str_len;

        if (*json != ':')
            return 0;
        else
            ++json;

        if (*json == ' ')
            ++json;

        str_len = is_valid_str(json);
        int digit_len = is_valid_num(json);

        if (str_len == 0 && digit_len == 0)
            return 0;
        else
            json += ((str_len == 0) ? digit_len : str_len);

        ++kv_count;

        if (*json == ',')
        {
            ++commas_count;
            ++json;
        }

        if (*json == ' ')
            ++json;
    }

    ++json;
    if (*json != '\0')
        return 0;

    return commas_count == (kv_count - 1);
}

int convert_str_to_num(const char *num, int len)
{
    int is_neg = 0;
    int i = 0;

    if (*num == '-')
    {
        is_neg = 1;
        ++i;
    }

    int res = 0;

    for (; i < len; ++i)
        res = res * 10 + (num[i] - '0');

    if (is_neg)
        res *= -1;

    return res;
}

static PyObject *
loads(PyObject *self, PyObject *args)
{
    const char *str;

    if (!PyArg_ParseTuple(args, "s", &str))
    {
        PyErr_Format(PyExc_TypeError, "Expected object or value");
        return NULL;
    }

    if (!is_json_valid(str))
    {
        PyErr_Format(PyExc_TypeError, "Expected object or value");
        return NULL;
    }

    PyObject *dict = NULL;
    if (!(dict = PyDict_New()))
    {
        printf("ERROR: Failed to create Dict Object\n");
        return NULL;
    }

    const char *temp = str + 1;

    while (*temp != '}')
    {
        PyObject *key = NULL;
        PyObject *value = NULL;

        int key_len = is_valid_str(temp);
        ++temp;

        if (!(key = Py_BuildValue("s#", temp, key_len - 2)))
        {
            printf("ERROR: Failed to build string value\n");
            return NULL;
        }

        temp += key_len + 1; // go to the value

        int val_len_num = is_valid_num(temp);
        int val_len_str = is_valid_str(temp);

        if (val_len_num > 0)
        {
            // use custom atoi because substr not null terminated
            int num = convert_str_to_num(temp, val_len_num);

            if (!(value = Py_BuildValue("i", num)))
            {
                printf("ERROR: Failed to build integer value\n");
                return NULL;
            }

            temp += val_len_num;
        }
        else if (val_len_str > 0)
        {
            ++temp;

            if (!(value = Py_BuildValue("s#", temp, val_len_str - 2)))
            {
                printf("ERROR: Failed to build string value\n");
                return NULL;
            }

            temp += val_len_str - 1; // cuz we are standing on str after "
        }

        if (PyDict_SetItem(dict, key, value) < 0)
        {
            printf("ERROR: Failed to set item\n");
            return NULL;
        }

        if (*temp == ',')
            ++temp;

        if (*temp == ' ')
            ++temp;
    }

    return dict;
}

static PyObject *
dumps(PyObject *self, PyObject *args)
{
    PyObject *dict;

    if (!PyArg_ParseTuple(args, "O!", &PyDict_Type, &dict))
    {
        PyErr_Format(PyExc_TypeError, "Expected dict");
        return NULL;
    }

    PyObject *key, *value;
    Py_ssize_t pos = 0;

    arr_t formed_str;
    arr_init(&formed_str);

    if (arr_append(&formed_str, '{'))
    {
        printf("ERROR: Memory allocation error\n");
        return NULL;
    }

    while (PyDict_Next(dict, &pos, &key, &value))
    {

        const char *s = NULL;

        if (!(s = PyUnicode_AsUTF8(key)))
        {
            PyErr_Format(PyExc_TypeError, "Expected string as a key");
            return NULL;
        }

        if (arr_append(&formed_str, '"'))
        {
            printf("ERROR: Memory allocation error\n");
            return NULL;
        }

        if (arr_append_seq(&formed_str, s))
        {
            printf("ERROR: Memory allocation error\n");
            return NULL;
        }

        if (arr_append(&formed_str, '"'))
        {
            printf("ERROR: Memory allocation error\n");
            return NULL;
        }

        if (arr_append_seq(&formed_str, ": "))
        {
            printf("ERROR: Memory allocation error\n");
            return NULL;
        }

        if (PyLong_CheckExact(value))
        {
            PyObject *value_repr = NULL;
            if (!(value_repr = PyObject_Repr(value)))
            {
                printf("ERROR: Cant get repr\n");
                return NULL;
            }

            const char *s = NULL;

            if (!(s = PyUnicode_AsUTF8(value_repr)))
            {
                printf("ERROR: Cant get str\n");
                return NULL;
            }

            if (arr_append_seq(&formed_str, s))
            {
                printf("ERROR: Memory allocation error\n");
                return NULL;
            }
        }
        else if ((s = PyUnicode_AsUTF8(value)))
        {
            if (arr_append(&formed_str, '"'))
            {
                printf("ERROR: Memory allocation error\n");
                return NULL;
            }

            if (arr_append_seq(&formed_str, s))
            {
                printf("ERROR: Memory allocation error\n");
                return NULL;
            }

            if (arr_append(&formed_str, '"'))
            {
                printf("ERROR: Memory allocation error\n");
                return NULL;
            }
        }
        else
        {
            PyErr_Format(PyExc_TypeError, "Expected string or num as a value");
            return NULL;
        }

        if (arr_append(&formed_str, ','))
        {
            printf("ERROR: Memory allocation error\n");
            return NULL;
        }

        if (arr_append(&formed_str, ' '))
        {
            printf("ERROR: Memory allocation error\n");
            return NULL;
        }
    }

    if (pos != 0)
    {
        formed_str.c[formed_str.len - 2] = '}';
        formed_str.c[formed_str.len - 1] = '\0';
    }
    else
    {
        if (arr_append(&formed_str, '}'))
        {
            printf("ERROR: Memory allocation error\n");
            return NULL;
        }

        if (arr_append(&formed_str, '\0'))
        {
            printf("ERROR: Memory allocation error\n");
            return NULL;
        }
    }

    PyObject *res_str = NULL;

    if (!(res_str = PyUnicode_FromString(formed_str.c)))
    {
        printf("ERROR: Cannot form string\n");
        return NULL;
    }

    arr_free(&formed_str);

    return res_str;
}

static PyMethodDef methods[] = {
    {"loads", loads, METH_VARARGS, "loads"},
    {"dumps", dumps, METH_VARARGS, "dumps"},
    {NULL, NULL, 0, NULL}};

static struct PyModuleDef module_cjson = {
    PyModuleDef_HEAD_INIT, "cjson", NULL, -1, methods};

PyMODINIT_FUNC PyInit_cjson()
{
    return PyModule_Create(&module_cjson);
}