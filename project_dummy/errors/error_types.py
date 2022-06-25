from .error_meta import BaseError, ErrorField, SerializedException


class ErrorCode(BaseError):
    SERVER_GENERAL_ERROR = ErrorField(500, "SERVER_GENERAL_ERROR", "通用错误")
    FETCH_META_ERROR = ErrorField(50001, "FETCH_META_ERROR", "获取实验元数据失败")
    PULL_DATA_ERROR = ErrorField(50100, "PULL_DATA_ERROR", "拉取数据错误")
    IMPUTE_ERROR = ErrorField(501, "IMPUTE_ERROR", "通用impute错误")
    IMPUTE_TYPE_ERROR = ErrorField(50101, "IMPUTE_TYPE_ERROR", "数值类型错误")
    IMPUTE_TIMEOUT_ERROR = ErrorField(50102, "IMPUTE_TIMEOUT_ERROR", "通用impute超时")
    IMPUTE_IO_ERROR = ErrorField(50103, "IMPUTE_IO_ERROR", "保存impute文件错误")
    IMPUTE_DB_ERROR = ErrorField(50104, "IMPUTE_DB_ERROR", "通用impute数据库错误")
    IMPUTE_RANGE_ERROR = ErrorField(50105, "IMPUTE_RANGE_ERROR", "数值不合理")
    FEATURE_PROCESS_ERROR = ErrorField(502, "FEATURE_PROCESS_ERROR", "特征预处理处理")
    FEATURE_TYPE_ERROR = ErrorField(50201, "FEATURE_TYPE_ERROR", "特征类型错误")
    FEATURE_ENCODER_ERROR = ErrorField(503, "FEATURE_ENCODER_ERROR", "FeatureEncoder模块错误")
    FEATURE_ENCODE_TIMEOUT = ErrorField(50302, "FEATURE_ENCODE_TIMEOUT", "编码超时")
    TRAIN_ERROR = ErrorField(504, "TRAIN_ERROR", "训练错误")
    TRAIN_RESOURCE_ERROR = ErrorField(50401, "TRAIN_RESOURCE_ERROR", "训练资源不够")
    TRAIN_TIMEOUT = ErrorField(50402, "TRAIN_TIMEOUT", "训练超时")
    TRAIN_PARAMETER_ERROR = ErrorField(50403, "TRAIN_PARAMETER_ERROR", "训练参数错误")
    GENERAL_ERROR = ErrorField(6001, "GENERAL_ERROR", "系统异常")


SerializedException.configure(ErrorCode, letter_case='short')
